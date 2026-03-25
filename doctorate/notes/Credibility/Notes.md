
- I think that we can solve the problem writing a $\lambda(p_s)$ such that increase when the gap is very low and that decreases when the gap is big: we kill the monotonicity of the best-response mapping for bad behaviors and we keep it for good behavior. We can check this from the RBSDE.
- We want to have that for $p \geq p'$ we have that  $$Y_s^{t,x;p} - h(s,X_s^{t,x},p) = U(s,x;p) \leq U(s,x;p') = Y_s^{t,x;p'} - h(s,X_s^{t,x},p')$$
- The RBSDE of the difference is given ![[Pasted image 20260209133441.png]] 
- The term $K'(p)\dot p$ is wrong, we should use $dK(p)$.
- We need to show that the martingale term is indeed a martingale and compare the obstacles.
- The above idea is working. With a $K(p)$ of the form  $$ K(p) = \frac{C}{1-\kappa p_t} $$ we have have indeed uniqueness (or be near to it).
- The driver can be shown to satisfies the require conditions whenever ![[Pasted image 20260209133602.png]]
- Under the above condition, we will have firms that will never switched - economically, the social cost of transition of making switching this firms is higher than the net benefit of these firms keep working with the bad technology (cost of switching, taxes pay). 
- what more can we say about the condition for uniqueness...?

19/02/2025


- Things to check
	![[Pasted image 20260219225249.png]]
- We have to check 
  ![[Pasted image 20260219225358.png]]
- We have
	- ![[Pasted image 20260220132322.png]]
	- we can have a clear relatioship upon parameters model to have this 
	- 