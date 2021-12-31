As noted in the AoC front matter, figuring out how hard a puzzle is hard.  I don't have a CS 
background, so I tend to "brute force" first.  It became apparent that a lot of the puzzles, 
especially the part 2's, were designed so that naive approaches weren't scalable.
Since I wasn't trying to get into the rankings, didn't always optimize things (or only optimized
up to the point of feasibility).  I think this made me think more about algorithm complexity when
starting out, although I still had some dead-end starts.

I appreciated the test inputs and examples that could be used as test inputs.  I think promoting a 
"test oriented" approach is good, even if the lifetime of each bit of code is very short.

Day 23 and 24 were definitely the ones I spent the longest on.  At some point, day 23 
just became super complicated and a huge time sink to implement the complex-ish rules.  Probably
there is some way to simplify the move rules, but I could not think of a way that covered all the
cases for moving in and out of the destinations.  It took me forever to finish part 1, but I failed
to plan for how they would expand for part 2, so I ended up rewriting my algorithm from scratch 
and having to debug it again.  Ugh.

In Day 24, it seemed like my search for the chain of Z values (starting at the last digit and
working backwards) would never converge, but I think it was just the slowness of the approach that
I took.  Fortunately, the search results could be used for both parts 1 and 2, so at least once they
were done, it was easy to get both solutions.  Looking at Reddit, it seemed like the way to speed
things up was to analyze the program contents more.  Some people said they had search-based solutions
that ran in sub-minute times, but by the time I got to the solution, I was over digging into it
anymore.

This was my first year for AoC, but I really enjoyed it.  Looking forward to next year.

