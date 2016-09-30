+++
date = "2016-08-26T20:20:39-07:00"
draft = true
title = "Thoughts on Locks (Part I)"

+++

<!--
Table of Contents
-----------------

1) Recursive Locks                     (this)
2) seqlock_T
3) rwlock_t
4) RCU
5) Software Transactional Memory
6) Message-based approach
7) Conclusion

-->

<!-- TODO: fix spaces between functions in code blocks -->
In this article we will walk through some common mistakes with regards to
locking and why <i>spinlock</i>s and <i>mutex</i>es suck in general. We will
discuss some alternatives and make a case for lock-less programming. Let's dive
in, it's going to be interesting.
<!--more-->
<strong>Please note: This is a draft</strong><br /><br />
Consider the following piece of simple code using Linux-kernel style locks:
<pre><code class="c">void
some_function()
{
	spin_lock(&some_global_lock);
	// some critical section magic
	spin_unlock(&some_global_lock);
	return;
}
</code></pre>

At first the code looks great, some structure is protected using a
<code>spin_lock_t</code>. However, there is a big problem. The said structure
is locked via a global lock, namely <code>some_global_lock</code>. What if
the critical section inside the lock calls code that locks the lock again?
You get a dreaded <strong>deadlock</strong>, oh no!

The programmer comes up with a "brilliant" concept:
<pre><code class="c">void
other_function()
{
	if(is_spin_locked(&some_global_lock))
		spin_lock(&some_global_lock);
	// another critical section
	spin_unlock(&some_global_lock);
	return;
}
</code></pre>
Can you spot the problem? How do you detect whether the lock was set when you
entered the function in order to decide whether to unlock the spinlock or leave
it alone? So, naturally the next thing that comes into mind is to increment
some internal counter everytime <code>spin_lock</code> is called by the same
thread, and decrement it each time <code>spin_unlock</code> is called. So, we
arrive at this code:

<pre><code class="c">void
other_function()
{
	spin_lock(&some_global_lock);
	// another critical section
	spin_unlock(&some_global_lock);
	return;
}

void
some_function()
{
	spin_lock(&some_global_lock);
	// some critical magic
	other_function();
	spin_unlock(&some_global_lock);
	return;
}
</code></pre>
Awesome, one may think! We can call both <code>other_function</code> and
<code>some_function</code> without having to worry about locks! That's epic!
No. These are called <i>recursive locks</i>. Please avoid them. They are wrong.
Just no.

So, let's discuss why the fact that using recursive locks is so bad. First and
foremost, the most crucial in mutual exclusion is the ability to run most of
the code in a parallel setting. Recursive locks do not encourage that. In fact,
they encourage you to be lazy and just lock everything you need. That sort of
encouragement essentially destroys what you wanted in the first place, that is
your code won't be parallel anymore. Instead, a well-behaved programmer would
do the following:

<pre><code class="c">void
other_function_unsafe()
{
	// critical section
}

void
other_function()
{
	spin_lock(&some_global_lock);
	other_function_unsafe();
	spin_unlock(&some_global_lock);
}

void
some_function()
{
	spin_lock(&some_global_lock);
	// some critical magic
	other_function_unsafe();
	spin_unlock(&some_global_lock);
}
</code></pre>
... which is a much nicer solution. We have the critical section
<i>thoughtfully</i> separated, and if we happen to need the same code while
under the same lock, we can reuse the code worry-free. This way of working
helps you enforce one of the most critical rules of threaded-programming:
<i>Keep critical sections as short as possible</i>.

Our solution is still far from perfect. What if Programmer B came along and
added a function call into <code>other_function_unsafe</code>? This shouldn't
be a problem <i>per-se</i>, but what if that function goes ridicolous and calls
a dozen others? That would again violate the rule we proposed earlier, not to
mention what if one of the functions that are called begins to sleep? This is a
<strong>deadlock</strong> waiting to strike. Even if we are lucky to avoid the
deadlock, we still have to account for starvation of other threads waiting on
this lock.

Obviously, the use of a global lock is a terrible practice as well, because
probably you started using threads as a form to implement to concurrency, but
using a single global lock does much damage to it, if not completely preventing
it. In the next part, we will cover fine-grained locking and all of its
benefits.
