# miqcp-planning

The skeleton notebook, draft notebook, and final notebook are due on Nov 15, Nov 29, Dec 6 respectively. 

Please find attached the set of readings for the project. We advice you to coordinate and set up regular meetings to go through the readings and sketch out the skeleton notebook. 

The most important readings are the L24.5 lecture, which shows you how to write trajectory planning as a mixed integer linear program. However, because we will impose speed limits on the vehicle, you will need to add quadratic constraints to limit how far the vehicle travels between time steps. This takes you into the realm of mix integer quadratically constrained programs (MIQCP). While the integer variables makes the problem combinatorial, once you make assignments to the integer variables, the remainder of the problem is a quadratically constrained program, a special subset of convex programs covered in L25. The L11 pdf is there for reference, since it presents ScottyConvexPath, another example of path planning using convex programs.

You will be responsible for breaking down the problem, first by introducing trajectory optimisation, then providing a MIQCP encoding of the problem, then briefly reviewing methods for solving convex programs, and finally solving the MIQCP encoding of a trajectory optimisation problem with a provided solver. We will provide you with examples code calling a MIQCP solver after you have submitted the skeleton notebook. 
