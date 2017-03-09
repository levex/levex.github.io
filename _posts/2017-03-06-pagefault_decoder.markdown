---
layout: post
title:  "Pagefault decoder"
date:   2017-03-05 12:00:00 +0000
categories: kernel
---

Hello,

often times I need to decode a pagefault error code, here is some JS to do
this, faster:

{% include pagefault_solver.html %}
