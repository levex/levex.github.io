---
layout: post
title:  "Pagefault decoder"
date:   2017-03-05 12:00:00 +0000
categories: kernel calculators
---

Many times over the past few years I've encountered Page Faults that due to
the nature of the environment, were only displayed in hexadecimal format. To
make these error codes human-readable, I've made a quick demo to let me do just
that.

<!-- MORE -->

Enter the error code, here, either in hexadecimal or in decimal notation and
the readable-string will be shown:

{% include pagefault_solver.html %}
