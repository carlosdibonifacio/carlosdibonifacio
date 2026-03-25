<TeXmacs|2.1.4>

<style|tmbook>

<\body>
  <doc-data|<doc-title|Mean field theory>|<doc-author|<author-data|<author-name|PSL
  Dauphine - M2 MATH/MASEF.>>>>

  <chapter|Analysis in the space of measures>

  <section|Space of measures>

  <paragraph|Space> Lets <with|font|cal|O> be a space, define a
  <math|\<sigma\>-algebra> on such space, denoted by <with|font|cal|A>. The
  space <with|font|cal|O> is a metric space but we don't define any topology
  by now. Define the measure\ 

  <\equation*>
    <math|\<mu\>:<with|font|cal|A> \<rightarrow\><with|font|Bbb|R>>\ 
  </equation*>

  and for <math|(A<rsub|i>)<rsub|i\<in\> I >\<in\> ><with|font|cal|A>
  pair-wise disjoint set we have that

  <\equation*>
    \<mu\><around*|(|\<cup\><rsup|N><rsub|i=1>A<rsub|i>|)>=<big|sum><rsub|i=1><rsup|n>\<mu\><around*|(|A<rsub|i>|)>
  </equation*>

  and <math|\<mu\>\<mapsto\>\<mu\><rsup|+>,\<mu\><rsup|->> and<math|
  \<mu\>=\<mu\><rsup|+>-\<mu\><rsup|->.>

  <paragraph|Total variation of the set of measures.>Defiene the total
  variation as\ 

  <\equation*>
    <around*|\||\<mu\>|\|><rsub|TV>\<assign\><around*|\||\<mu\>|\|><around*|(|<with|font|cal|O>|)>
  </equation*>

  and define also\ 

  <\equation*>
    <around*|\||\<mu\>|\|>\<assign\>\<mu\><rsup|+>+\<mu\><rsup|->
  </equation*>

  <\theorem>
    (<with|font|cal|M>(<with|font|cal|O>),<math|<around*|\||\<cdot\>|\|><rsub|TV>>)
    is a Banact (complete) space.
  </theorem>

  <paragraph|Action of functions.>The topoply induced by <math|the TV> norm
  is such that for <math|\<delta\><rsub|x>> and <math|\<delta\><rsub|y>> for
  <math|x\<neq\>y> we have that <math|<around*|\||\<delta\><rsub|x>-\<delta\><rsub|y>|\|><rsub|TV>=2.>
  Mass that can be very near can be veyr far using such nrom..

  <\definition>
    Weakly convergence. Let <math|(<math|\<mu\><rsub|n>>)<rsub|n\<geq\>0> >
    be a sequence in <math|<with|font|cal|M><around*|(|<with|font|cal|O>|)>.
    We say that > <math|(<math|\<mu\><rsub|n>>)<rsub|n\<geq\>0> > weakly
    converges to <math|\<mu\>> if for any bounded continuos function i.e.
    <math|\<varphi\>>\<in\> <math|C<rsub|b><around*|(|<with|font|cal|O>|)>>
    we have that

    <\equation*>
      lim<rsub|n\<rightarrow\>\<infty\>><big|int>\<varphi\><math-up|d>\<mu\><rsub|n>\<rightarrow\><big|int>\<varphi\><math-up|d>\<mu\><rsub|>
    </equation*>

    \;
  </definition>

  <\remark>
    The topology induced by the TV norm does not concidie with the topology
    induced<space|1em>by the weak-convergence.
  </remark>

  <paragraph|Couplings, disingetation and gluing.>

  <paragraph|Wasserstein distance. >We define the set of probability measure
  with p-th moment finite as\ 

  <\equation*>
    <with|font|cal|P><rsub|p><around*|(|<with|font|cal|O>|)>=<around*|{|\<mu\>\<in\><with|font|cal|P><rsub|><around*|(|<with|font|cal|O>|)>:<big|int><rsub|<with|font|cal|O>>d<around*|(|x<rsub|0>,x|)><rsup|p
    >\<mu\><around*|(|<text|d>x|)>\<less\>\<infty\> |}>.
  </equation*>

  We want to metrize the weak-convergence. Consider <math|p\<in\>
  <around*|(|1,+\<infty\>|)>,we define the Wasserstein distance as>

  <\eqnarray*>
    <tformat|<table|<row|<cell|W<rsub|p><around*|(|\<mu\>,\<nu\>|)>>|<cell|=>|<cell|inf<rsub|\<pi\>\<in\>
    \<Pi\><around*|(|\<mu\>,\<nu\>|)>><around*|(|<big|int><rsub|<with|font|cal|O>\<times\>O>d<around*|(|x,y|)><rsup|p>\<pi\><around*|(|<text|d>x,<text|d>y|)>|)><rsup|<frac|1|p>>>>|<row|<cell|>|<cell|=>|<cell|inf<rsub|X\<sim\>\<mu\>,Y\<sim\>\<nu\>>
    <with|font|Bbb|E><around*|[|<around*|\||X-Y|\|><rsup|p>|]>>>>>
  </eqnarray*>

  <\theorem>
    We have the following results:

    <\enumerate-roman>
      <item>The space <math|(<with|font|cal|<math|P>><rsub|p><around*|(|<with|font|cal|O>|)>,W<rsub|p>)>
      is a complete separable metric space.

      <item><math|\<forall\>\<mu\>,\<nu\>>\<in\><math|<with|font|cal|<math|P>><rsub|p><around*|(|<with|font|cal|O>|)>>,
      the <math|inf>is always reached.
    </enumerate-roman>
  </theorem>

  <\remark>
    For <math|p\<leq\>p'> we have that <math|W<rsub|p>\<leq\>W<rsub|p<rprime|'>>.>
  </remark>

  <\theorem>
    Kantorovich distance. For all <math|\<mu\>,\<nu\>\<in\>><math|<with|font|cal|<math|P>><rsub|1><around*|(|<with|font|cal|O>|)>,>
    we have

    <\eqnarray*>
      <tformat|<table|<row|<cell|W<rsub|1><around*|(|\<mu\>,\<nu\>|)>>|<cell|=>|<cell|sup<rsub|<around*|\<\|\|\>|\<phi\>|\<\|\|\>><rsub|Lips.>\<leq\>1><big|int>\<phi\><around*|(|d\<mu\>-\<nu\>|)>>>|<row|<cell|>|<cell|=>|<cell|<around*|\<\|\|\>|\<mu\>-\<nu\>|\<\|\|\>><rsub|W<rsup|1,1>>>>>>
    </eqnarray*>

    \;
  </theorem>

  <\theorem>
    Sia <math|<around*|(|\<mu\><rsub|n>|)><rsub|n\<geq\>0>
    \<in\><with|font|cal|P><rsub|p><around*|(|<with|font|cal|O>|)> >and
    <math|\<mu\>><math|\<in\><with|font|cal|P><rsub|p><around*|(|<with|font|cal|O>|)>
    . >We have that

    <\equation*>
      lim<rsub|n\<rightarrow\>\<infty\>>W<rsub|p><around*|(|\<mu\><rsub|n>,\<mu\>|)>=0\<Leftrightarrow\><choice|<tformat|<table|<row|<cell|\<mu\><rsub|n>\<rightarrow\><rsup|>\<mu\>>>|<row|<cell|<big|int><rsub|<with|font|cal|O>>d<around*|(|x<rsub|o>,x|)><rsup|p>\<mu\><rsub|n><around*|(|d<text|x>|)>\<rightarrow\><big|int><rsub|<with|font|cal|O>>d<around*|(|x<rsub|o>,x|)><rsup|p>\<mu\><rsub|><around*|(|d<text|x)><rsub|>|\<nobracket\>>>>>>>
    </equation*>

    and also\ 

    <\equation*>
      lim<rsub|n\<rightarrow\>\<infty\>>W<rsub|p><around*|(|\<mu\><rsub|n>,\<mu\>|)>=0\<Leftrightarrow\>lim<rsub|n\<rightarrow\>\<infty\>><big|int><rsub|<with|font|cal|O>>\<phi\><around*|(|x|)>\<mu\><rsub|n><around*|(|d<text|x>|)>=<big|int><rsub|<with|font|cal|O>>\<phi\><around*|(|x|)>\<mu\><rsub|><around*|(|d<text|x>|)>
    </equation*>

    for any function <math|\<phi\> >such that
    <math|\|<math|\<phi\><around*|(|x|)>>\|\<leq\>C(1+<around*|\||x|\|><rsup|p>)>.
  </theorem>

  <paragraph|Lifting.>Let <math|U<rsub|>:<with|font|cal|P><rsub|p><around*|(|<with|font|Bbb|R<rsup|d>>|)>\<rightarrow\><with|font|Bbb|R<rsup|>>>,
  we can define the lift as\ 

  <\eqnarray*>
    <tformat|<table|<row|<cell|<wide|U|^>>|<cell|:>|<cell|L<rsup|p><around*|(|\<Omega\>,<with|font|Bbb|R<rsup|d>>|)>\<rightarrow\><with|font|Bbb|R>>>|<row|<cell|>|<cell|>|<cell|X
    \<rightarrow\>U<around*|(|<with|font|cal|L><around*|(|X|)>|)>>>>>
  </eqnarray*>

  For <math|p>=2, <math|L<rsup|2>> is a Hilbert space.

  \;

  <\lemma>
    For <math|X,X<rprime|'>> random variables such that
    <math|<with|font|cal|L><around*|(|X|)>=<with|font|cal|L><around*|(|X<rprime|'>|)>,there
    is a measure preserving mapping >\<tau\>:\<Omega\>
    \<rightarrow\>\<Omega\> such that <math|\|<around*|\<\|\|\>|X<rsub|0>Z-X|\<\|\|\>><rsub|\<infty\>>\<less\>\<varepsilon\>.>
  </lemma>

  <section|variations>

  <paragraph|Linear variations.>

  <paragraph|Action of flows ODE.>

  <paragraph|Action of flows SDE.>

  <paragraph|Following couple.>

  <section|Derivative in the space of measure.>

  We have <math|U:<around*|(|<with|font|cal|M><around*|(|<with|font|cal|O>|)>,<around*|\||\<cdot\>|\|><rsub|TV>|)>\<rightarrow\><with|font|Bbb|R>>.
  We will recall the definition of Fréchet and Gateux differentiability.

  <\definition>
    Fréchet differentiability. The function U is said to have a Fréchet
    derivative at <math|><math|\<mu\><rsub|0>\<in\>
    <with|font|cal|M><around*|(|<with|font|cal|O>|)>, if >there is a there
    exists a <strong|bounded linear functional>

    <\equation*>
      D U<around*|(|\<mu\><rsub|0>|)><around*|[|\<nu\>|]>
    </equation*>

    such that we have

    \;

    <\equation*>
      lim<rsub|<around*|\<\|\|\>|\<nu\>|\<\|\|\>><rsub|TV>\<rightarrow\>0><frac|U<around*|(|\<mu\><rsub|0>+\<nu\>|)>-U<around*|(|\<mu\><rsub|0>|)>-D
      U<around*|(|\<mu\><rsub|0>|)><around*|[|\<nu\>|]>|<around*|\<\|\|\>|\<nu\>|\<\|\|\>>>=0.
    </equation*>

    where by Riesz representation theorem, we can write <math|D
    U<around*|(|\<mu\>|)><around*|[|\<nu\>|]>=<big|int><rsub|<with|font|cal|><with|font|cal|O>>\<phi\><rsub|\<mu\><rsub|0>>d\<nu\>>
    for some bounded measurable function <math|\<phi\><rsub|.>>
  </definition>

  <\remark>
    The Frèchet derivate is a bounded linear function, by duality, we have
    that <math|(<math|<with|font|cal|M><around*|(|<with|font|cal|O>|)>>)<rsup|*\<ast\>>
    \<simeq\>><math|<rsup|*><rsup|**>> <math|L<rsup|\<infty\>><around*|(|<with|font|cal|O>|)>>
    and thus by RPT we have that <math|\<phi\><rsub|\<mu\><rsub|0>>> is the
    unique function (a.e.) such that <math|D
    U<around*|(|\<mu\><rsub|0>|)><around*|[|\<nu\>|]>=><math|<big|int><rsub|<with|font|cal|><with|font|cal|O>>\<phi\><rsub|\<mu\><rsub|0>>d\<nu\>.>
  </remark>

  <\remark>
    <math|Heuristically,\<phi\><rsub|\<mu\><rsub|0>>> is interpeted as how
    much the functional <math|U> changes if you add an infinitesimal amount
    of mass at the point <math|x>. Consider a small pertubation
    <math|\<nu\>=\<varepsilon\>\<delta\><rsub|x>> and then

    <\equation*>
      U<around*|(|\<mu\><rsub|0>+\<varepsilon\>\<delta\><rsub|x>|)>=U<around*|(|\<mu\><rsub|0>|)>+\<varepsilon\>\<phi\><rsub|\<mu\><rsub|0>><around*|(|x|)>+o<around*|(|\<varepsilon\>|)>,
    </equation*>

    thus we have that

    <\equation*>
      \<phi\><rsub|\<mu\><rsub|0>><around*|(|x|)>=<math-up|<frac|d|d<math|\<varepsilon\>>>>U<around*|(|\<mu\><rsub|0>+\<varepsilon\>\<delta\><rsub|x>|)><around*|\||<rsub|\<varepsilon\>=0>|\<nobracket\>>.
    </equation*>
  </remark>

  <\definition>
    Gateux differentiability. The function U is said to have a Gateux
    derivative at <math|><math|\<mu\><rsub|0>>, if for all <math|\<nu\>\<in\>
    ><with|font|cal|M>(<with|font|cal|O>), there e

    <\equation*>
      lim<rsub|t<rsub|>\<rightarrow\>0><frac|U<around*|(|\<mu\><rsub|0>+\<nu\>|)>-U<around*|(|\<mu\>|)>|t>=<big|int>\<phi\><rsub|\<mu\><rsub|0>>d\<nu\>.
    </equation*>

    where <math|D U<around*|(|\<mu\>|)><around*|[|\<nu\>|]>=<big|int><rsub|<with|font|cal|><with|font|cal|O>>\<phi\><rsub|\<mu\>>d\<nu\>>.
  </definition>

  <\proposition>
    If <math|(m<rsub|t>):t\<rightarrow\>m<rsub|t> > is <math|C<rsup|1 \ >>,
    that is with respect to the total variation norm,, U is vertically
    differentiable at <math|m<rsub|0>> (as defined before), then
    U(<math|m<rsub|0> >) is differentiable at <math|0> and\ 

    <\equation*>
      <frac|<math-up|d>|dt>U<around*|(|m<rsub|t>|)>=
      <big|int><rsub|<with|font|cal|><with|font|cal|O>>\<nabla\>\<mu\>U<around*|(|m<rsub|0>|)><around*|(|x|)><wide|m|\<dot\>><around*|(|d
      x|)>.
    </equation*>
  </proposition>

  Intuitively, <math|(U)> assigns a number to an entire distribution of mass,
  and the function <math|( \<nabla\>\<mu\> U(m<rsub|0>)(x)> tells you how
  sensitive that number is to adding a tiny amount of mass at the point
  <math|(x).> When the measure <math|(m<rsub|t>)> evolves in time, its
  derivative <math|(<math|<wide|m<rsub|0>|\<dot\>>>)> describes where mass is
  increasing or decreasing and at what rate. The formula

  <\equation*>
    <frac|<math-up|d>|dt>U<around*|(|m<rsub|t>|)>=
    <big|int><rsub|<with|font|cal|><with|font|cal|O>>\<nabla\>\<mu\>U<around*|(|m<rsub|0>|)><around*|(|x|)><wide|m|\<dot\>><around*|(|d
    x|)>.
  </equation*>

  simply says that the total rate of change of <math|(U)> is obtained by
  combining, at each point <math|(x)>, how much <math|(U)> \Pcares\Q about
  mass there with how fast the mass is changing there, and then summing this
  effect over the whole space. This is the exact analogue of the usual chain
  rule\ 

  <\equation*>
    <math|><math|<frac|<math-up|d>|dt>f<around*|(|x<around*|(|t|)>|)>=><math|\<nabla\>f<around*|(|x<rsub|0>|)>\<cdot\><wide|x<rsub|0>|\<dot\>>>,
  </equation*>

  but with vectors replaced by measures and the dot product replaced by an
  integral. The presence of the integral is due to the fact in the measure
  setting you are differentiaing with respect to infintelty many degrees of
  freedom, while in the \Pnormal\Q finite-dimensional case you only have
  finitely many.

  <\definition>
    <dueto|Vertical derivative on <math|\<cal-P\><around|(|\<cal-O\>|)>>>Let
    <math|\<cal-O\>\<subset\>\<bbb-R\><rsup|d>> be a Borel set and let

    <\equation*>
      U:\<cal-P\><around|(|\<cal-O\>|)>\<to\>\<bbb-R\>
    </equation*>

    be a functional. We say that <math|U> is <em|vertically differentiable
    at> <math|\<mu\>\<in\>\<cal-P\><around|(|\<cal-O\>|)>> if there exists a
    function

    <\equation*>
      \<partial\><rsub|\<mu\>>*U<around|(|\<mu\>|)>\<in\>L<rsup|\<infty\>><around|(|\<cal-O\>|)>
    </equation*>

    such that

    <\equation*>
      lim<rsub|\<nu\>\<to\>\<mu\>> <frac|U<around|(|\<nu\>|)>-U<around|(|\<mu\>|)>-<with|math-display|true|<big|int><rsub|\<cal-O\>>\<partial\><rsub|\<mu\>>*U<around|(|\<mu\>|)><around|(|x|)>*<space|0.17em>d*<around|(|\<nu\>-\<mu\>|)><around|(|x|)>>|<around|\<\|\|\>|\<nu\>-\<mu\>|\<\|\|\>><rsub|T*V>>=0,
    </equation*>

    where the limit is taken over <math|\<nu\>\<in\>\<cal-P\><around|(|\<cal-O\>|)>>
    converging to <math|\<mu\>> in the total variation norm.
  </definition>

  <\definition>
    <dueto|Horizontal differentiability>Let
    <math|\<cal-O\>\<subset\>\<bbb-R\><rsup|d>> be open and let

    <\equation*>
      U:\<cal-P\><around|(|\<cal-O\>|)>\<to\>\<bbb-R\>.
    </equation*>

    We say that <math|U> is <em|horizontally differentiable at>
    <math|\<mu\>\<in\>\<cal-P\><around|(|\<cal-O\>|)>> if there exists a
    vector field

    <\equation*>
      \<nabla\><rsub|x>*\<partial\><rsub|\<mu\>>*U<around|(|\<mu\>|)>\<in\>L<rsup|p><around|(|\<cal-O\>,\<mu\>;\<bbb-R\><rsup|d>|)>*<space|1em><text|for
      some >p\<ge\>1,
    </equation*>

    such that for all <math|\<xi\>\<in\>C<rsub|c><rsup|\<infty\>><around|(|\<cal-O\>;\<bbb-R\><rsup|d>|)>>,

    <\equation*>
      lim<rsub|\<varepsilon\>\<to\>0> <frac|U*<around*|(|<around|(|I*d+\<varepsilon\>*\<xi\>|)><rsub|#>*\<mu\>|)>-U<around|(|\<mu\>|)>-\<varepsilon\>*<big|int><rsub|\<cal-O\>>\<nabla\><rsub|x>*\<partial\><rsub|\<mu\>>*U<around|(|\<mu\>|)><around|(|x|)>\<cdot\>\<xi\><around|(|x|)>*<space|0.17em>d*\<mu\><around|(|x|)>|<around|\<\|\|\>|\<xi\>|\<\|\|\>><rsub|L<rsup|p><around|(|\<mu\>|)>>>=0,
    </equation*>

    where

    <\equation*>
      <around|\<\|\|\>|\<xi\>|\<\|\|\>><rsub|L<rsup|p><around|(|\<mu\>|)>>=<around*|(|<big|int><rsub|\<cal-O\>><around|\||\<xi\><around|(|x|)>|\|><rsup|p>*<space|0.17em>d*\<mu\><around|(|x|)>|)><rsup|1/p>.
    </equation*>
  </definition>

  The vertical and horizontal derivatives describe two fundamentally
  different ways of changing a probability distribution. The <strong|vertical
  derivative> looks at what happens when you change <em|how much mass> is
  assigned to different locations while keeping the locations themselves
  fixed\Vmass is taken from some points and given to others. It measures how
  sensitive the functional is to the amount of mass at each point, which is
  why it is only defined up to an additive constant. In contrast, the
  <strong|horizontal derivative> looks at what happens when you keep the mass
  the same but <em|move it in space>, by slightly shifting the positions of
  the particles that make up the distribution. It measures how sensitive the
  functional is to where the mass is located, and therefore captures spatial
  effects. In short, vertical derivatives correspond to redistributing mass,
  while horizontal derivatives correspond to transporting mass.

  \;

  \;

  <chapter|Mean field Control>

  We have the control problem:

  <\equation*>
    <choice|<tformat|<table|<row|<cell|u<around*|(|t,\<mu\>|)>=inf<rsub|<around*|(|Z<rsub|s>|)><rsub|\<geq\>0>>
    <with|font|Bbb|E><around*|[|<big|int><rsub|t><rsup|T>L<around*|(|X<rsub|s>,Z<rsub|s>,<with|font|cal|L><around*|(|X<rsub|s>|)>|)>ds+G<around*|(|<with|font|cal|L><around*|(|X<rsub|T>|)>|)>|]>>>|<row|<cell|X<rsub|>\<sim\>\<mu\>>>|<row|<cell|X<rsub|1>=<big|int><rsub|t><rsup|1>Z<rsub|s>du>>|<row|<cell|u:<around*|[|0,T|]>\<times\><with|font|cal|P<rsub|>><rsub|2><around*|(|<with|font|cal|O>|)>\<rightarrow\><with|font|Bbb|R>>>>>>.
  </equation*>

  <\proposition>
    (Dynamic Programming Principle) - Let <math|t \<in\><around*|[|0,T|)>>,
    <math|\<mu\>\<in\> <with|font|cal|P<rsub|>><rsub|2><around*|(|<with|font|cal|O>|)>>,
    u

    <\equation*>
      u<around*|(|t,\<mu\>|)>=inf<rsub|<around*|(|Z<rsub|s>|)><rsub|\<geq\>0>>
      <with|font|Bbb|E><around*|[|<big|int><rsub|t><rsup|t+s>L<around*|(|X<rsub|s>,Z<rsub|s>,<with|font|cal|L><around*|(|X<rsub|s>|)>|)>ds+u<around*|(|t+s,<with|font|cal|L><around*|(|X<rsub|t+s>|)>|)>|]>.
    </equation*>

    \;
  </proposition>

  <\proof>
    U is smoothly<space|1em>

    \;
  </proof>

  <chapter|Mean Field Games>

  Consider the control problem:

  <\equation*>
    <with|font|Bbb|E><around*|[|<big|int><rsub|0><rsup|T>L<around*|(|X<rsub|t>,\<alpha\><rsub|t>|)>+f<around*|(|m<rsub|t>|)><around*|(|X<rsub|t>|)>dt+G<around*|(|m<rsub|T>|)><around*|(|X<rsub|T>|)>|]>
  </equation*>

  subject to the dynamics of <math|X<rsub|t>,>

  <\equation*>
    dX<rsub|t>=\<alpha\><rsub|t>dt+\<sigma\>dW<rsub|t>,X<rsub|0>=X
  </equation*>

  The MFG system is a system of coupled backward-forward PDEs.\ 

  \;

  \;

  <section|Forward-Backward equations>

  <subsection|Backward equation>

  In this case, we assume that the players knows or guess the trajectory
  <math|<around*|(|m<rsub|t>|)><rsub|t\<geq\>0>.> The player then solve the
  classic control problem

  <\equation*>
    <choice|<tformat|<table|<row|<cell|-\<partial\><rsub|t>u-<frac|\<sigma\><rsup|2>|2>\<Delta\><rsub|x>u+H<around*|(|\<alpha\>,\<nabla\><rsub|x>u|)>=f<around*|(|m<rsub|>|)><around*|(|x|)>,<around*|(|0,x|)>\<in\><around*|(|0,T|)>\<times\><with|font|Bbb|><with|font|Bbb|R><rsup|d>>>|<row|<cell|u<rsub|<around*|\|||\<nobracket\>>t=T>=G<around*|(|m<rsub|T>|)>>>>>>
  </equation*>

  where <math|<wide|\<alpha\><rsub|t>|^>=-D<rsub|p>H<around*|(|X<rsub|t>,D|)>>

  <subsection|Forward equation>

  We suppose now that the agents play or follow some strategy<math|/control>
  described by a smooth function of the form
  <math|b:<around*|[|0,T|]>\<times\>><with|font|Bbb|R><math|<rsup|d>\<rightarrow\>><with|font|Bbb|
  R><math|<rsup|d>>. The evolution of the distribution of the agents
  following such control is given by<\footnote>
    If we had

    <\equation*>
      <choice|<tformat|<table|<row|<cell|-\<partial\><rsub|t>\<mu\><rsub|t>-<frac|\<sigma\><rsup|2>|2>\<Delta\><rsub|>\<mu\><rsub|t>+div<around*|(|b\<mu\>|)>=\<rho\>>>|<row|<cell|\<mu\><rsub|<around*|\|||\<nobracket\>>t=0>=\<mu\><rsub|0>>>>>>
    </equation*>

    \ then we have players entering (or leaving) the game.
  </footnote>

  \;

  <\equation*>
    <choice|<tformat|<table|<row|<cell|-\<partial\><rsub|t>\<mu\><rsub|t>-<frac|\<sigma\><rsup|2>|2>\<Delta\><rsub|>\<mu\><rsub|t>+div<around*|(|b\<mu\>|)>=0
    >>|<row|<cell|\<mu\><rsub|<around*|\|||\<nobracket\>>t=0>=\<mu\><rsub|0>>>>>>
  </equation*>

  We know that the solution of the above equation is the function describing
  the evolution of the distribution of the law of the process

  <\equation*>
    dX<rsub|t><rsup|i>=b<around*|(|t,X<rsub|t><rsup|i>|)>dt+\<sigma\>dW<rsub|t><rsup|i>
  </equation*>

  where <math|<around*|(|W<rsub|t><rsup|i>|)><rsub|t\<leq\>i>,X<rsup|i><rsub|0<rsup|>>>

  \;

  <\equation*>
    lim<rsub|n\<rightarrow\>\<infty\>><big|sum><rsub|i=1><rsup|n>\<delta\><rsub|X<rsup|i><rsub|t>>=m<rsub|0>
  </equation*>

  and by Gliveno<math|->Cantelli's Law of Large Numbers, we have

  <\equation*>
    \<mu\><rsub|t><rsup|N>=<frac|1|N><big|sum><rsup|N><rsub|i=1>\<delta\><rsub|X<rsub|t><rsup|i>>\<rightarrow\>\<mu\><rsub|t>
    \ as N\<rightarrow\>\<infty\>
  </equation*>

  \;

  <subsection|Fokker-Planck Equation and mass conservation>

  Let <math|\<sigma\>=0>, <math|d=1> and that <math|b\<geq\>0.> Define by
  <math|m<around*|(|t,i|)>> as the number of players in state <math|i> at
  time <math|t.> We have <math|m<around*|(|t+d t, i|)>. >See that\ 

  <\equation*>
    m<around*|(|t+d t, i|)>=m<around*|(|t,i|)>+<wide*|m<around*|(|t,i-1|)>d
    t\<cdot\><frac|b<around*|(|t,i-1|)>|d
    x>|\<wide-underbrace\>><rsub|players entering the state
    i>-<wide*|m<around*|(|t,i|)>d t\<cdot\><frac|b<around*|(|t,i|)>|d
    x>|\<wide-underbrace\>><rsub|players \ leaving the state \ i>
  </equation*>

  \;

  <math|>The discretized equation represents a local conservation of mass
  across neighbouring spatial cells. Space is divided into intervals of size
  <math|\<Delta\>x>, and <math|m(t,i)> denotes the number of players located
  in cell i at time t. Over a small time interval dt, players move
  deterministically with velocity <math|b(t,x) \<geq\> 0>, so transitions
  occur only from cell <math|i> to cell<math| i+1>. The quantity
  <math|b(t,i)> dt divided by <math|\<Delta\>x> represents the fraction of
  players in cell i that cross the right boundary during the time step dt.
  Consequently, the mass in cell i at time <math|t+d t> equals the current
  mass plus the inflow coming from cell <math|i\<minus\>1>, minus the outflow
  leaving toward cell <math|i+1>. The inflow is proportional to the number of
  players in the neighbouring cell multiplied by their velocity, while the
  outflow depends on the mass currently present in cell i. The equation
  therefore expresses a discrete balance law: the change of mass in each
  state equals inflow minus outflow. When the spatial and temporal steps go
  to zero, this discrete conservation rule converges to the continuous
  conservation equation describing the transport of the population density,
  which corresponds to the zero-diffusion case of the Fokker\UPlanck
  equation.

  \;

  <\equation*>
    \<partial\><rsub|t>m=-\<partial\>x<around*|(|m b|)>.
  </equation*>

  The <strong|Laplacian> in the Fokker\UPlanck equation represents the effect
  of <strong|random motion spreading probability mass> in space. While the
  drift term transports mass deterministically along trajectories, the
  Laplacian accounts for the dispersion created by stochastic fluctuations.
  More precisely, when particles follow a diffusion process, random shocks
  continuously push them in all directions. This produces a net movement of
  probability from regions of high density toward regions of low density.
  Mathematically, this phenomenon is described by the Laplacian operator
  acting on the density. The Laplacian measures local curvature: if the
  density is locally peaked, the Laplacian is negative and mass spreads
  outward; if the density is locally low relative to its surroundings, the
  Laplacian is positive and mass flows inward. As a result, the Laplacian
  generates a smoothing effect, progressively regularizing the distribution
  over time.

  \;

  <\eqnarray*>
    <tformat|<table|<row|<cell|m<around*|(|t+d t,
    i|)>>|<cell|=>|<cell|m<around*|(|t,i|)>>>|<row|<cell|>|<cell|>|<cell|+<space|1em>
    <wide*|m<around*|(|t,i-1|)>d t\<cdot\><frac|b<around*|(|t,i-1|)>|d
    x>|\<wide-underbrace\>><rsub|players entering the state
    i><space|1em>-<wide*|m<around*|(|t,i|)>d
    t\<cdot\><frac|b<around*|(|t,i|)>|d x>|\<wide-underbrace\>><rsub|players
    \ leaving the state \ i>>>|<row|<cell|>|<cell|>|<cell|+<space|1em>
    <wide*|<frac|\<sigma\><rsup|2>|2><frac|d t|<around*|(|d
    x|)><rsup|2>><around*|(|m<around*|(|t,i+1|)>-2m<around*|(|t,i|)>+m<around*|(|t,i-1|)>|)>|\<wide-underbrace\>><rsub|stochastic
    \ inflow<infix-and>outflow of players>>>>>
  </eqnarray*>

  when taking the limit, we have

  \;

  <\equation*>
    \<partial\><rsub|t>m+\<partial\>x<around*|(|m b|)>=
    <frac|\<sigma\><rsup|2>|2>\<partial\><rsub|x x><rsup|>m
  </equation*>

  The Laplacian term in the Fokker\UPlanck equation originates from the
  presence of random motion at the microscopic level. When particles or
  agents move purely deterministically, their distribution is simply
  transported in space by the velocity field. However, when their motion
  contains small unpredictable fluctuations \V such as shocks, noise, or
  individual randomness \V each particle continuously performs tiny random
  displacements in all directions. Over a short time interval, the density at
  a given location therefore becomes an average of the densities in nearby
  locations, since particles arriving there come from surrounding points
  rather than from a single deterministic trajectory. Because these random
  displacements are symmetric, there is no net first-order movement in any
  direction; instead, the dominant effect comes from how the density locally
  differs from its neighbourhood. The Laplacian mathematically measures
  exactly this local imbalance between a point and the average of its
  surroundings. If the density is locally concentrated, random motion spreads
  mass outward; if it is locally low, surrounding particles tend to fill the
  region. In this way, the Laplacian represents the macroscopic effect of
  many small independent random movements, producing diffusion, smoothing the
  distribution over time, and preserving the total mass while redistributing
  it spatially.

  \;

  <section|Nash equilbrium and the MFG system.>

  <\definition>
    A NE is a strategy <math|b:<around*|[|0,T|]>\<times\><with|font|Bbb|R><rsup|d>\<rightarrow\><with|font|Bbb|<with|font|Bbb|R><rsup|d><rsup|>>>
    such that <math|b >is the best-response of the trajectory
    <math|(<math|\<mu\><rsub|t>>)<rsub|t\<geq\>0>><math|> which is the unique
    solution to

    \;

    <\equation*>
      <choice|<tformat|<table|<row|<cell|-\<partial\><rsub|t>\<mu\><rsub|t>-<frac|\<sigma\><rsup|2>|2>\<Delta\><rsub|>\<mu\><rsub|t>+div<around*|(|b\<mu\>|)>=0
      >>|<row|<cell|\<mu\><rsub|<around*|\|||\<nobracket\>>t=0>=\<mu\><rsub|0>>>>>>
    </equation*>

    and <math|b> is obtained from solving

    <\equation*>
      <choice|<tformat|<table|<row|<cell|-\<partial\><rsub|t>u-<frac|\<sigma\><rsup|2>|2>\<Delta\><rsub|x>u+H<around*|(|\<alpha\>,\<nabla\><rsub|x>u|)>=f<around*|(|\<mu\><rsub|>|)><around*|(|x|)>,<around*|(|0,x|)>\<in\><around*|(|0,T|)>\<times\><with|font|Bbb|><with|font|Bbb|R><rsup|d>>>|<row|<cell|u<rsub|<around*|\|||\<nobracket\>>t=T>=G<around*|(|\<mu\><rsub|T>|)>>>>>>
    </equation*>
  </definition>

  \;

  <\definition>
    A NE is a solution <math|<around*|(|u,m|)> \ of the system:>

    <\equation*>
      <choice|<tformat|<table|<row|<cell|
      -\<partial\><rsub|t>u-<frac|\<sigma\><rsup|2>|2>\<Delta\><rsub|x>u+H<around*|(|\<alpha\>,\<nabla\><rsub|x>u|)>=f<around*|(|m|)><around*|(|x|)>>>|<row|<cell|-\<partial\><rsub|t>m<rsub|t>-<frac|\<sigma\><rsup|2>|2>\<Delta\><rsub|>m<rsub|t>+div<around*|(|b
      m|)>=0>>|<row|<cell|b=-D<rsub|p>H<around*|(|x,\<nabla\><rsub|x>u<around*|(|t,x|)>|)>>>|<row|<cell|u<rsub|<around*|\||t=T|\<nobracket\>>>G<around*|(|m<rsub|T>|)>,m<rsub|0>
      given.>>>>>
    </equation*>
  </definition>

  <subsection|Existence>

  Existence is usually showed using a fixed point result and its done as a
  fixed point of the function <math|m>. Compactedness is needed to use the
  theorem, what is usually achived by some estimates arguments.

  <subsection|Uniqueness>

  <\theorem>
    Assume that H is convex and that <math|f> and <math|g> <math|define as
    function <with|font|cal|P><around*|(|<with|font|Bbb|R><rsup|d>|)>\<rightarrow\>C<around*|(|<with|font|Bbb|R<rsup|d>>|)>
    >are monotone functions. Moreover, assume that <math|f> is strictly
    motone. That is, for and g and f:

    <\equation*>
      <big|int><rsub|<with|font|Bbb|R><rsup|d>><around*|(|g<around*|(|m|)><around*|(|x|)>-g<around*|(|m<rprime|'>|)><around*|(|x|)>|)><around*|(|m-m<rprime|'>|)>d<around*|(|x|)>\<geq\>
      0
    </equation*>

    <\equation*>
      <big|int><rsub|<with|font|Bbb|R><rsup|d>><around*|(|f<around*|(|m|)><around*|(|x|)>-f<around*|(|m<rprime|'>|)><around*|(|x|)>|)><around*|(|m-m<rprime|'>|)>d<around*|(|x|)>\<gtr\>
      0
    </equation*>

    Then, there xist at most one solution <math|<around*|(|u,m|)>> of the MFG
    system.

    <\equation*>
      \;
    </equation*>
  </theorem>

  <\proof>
    Take 2 solutions <math|<around*|(|u<rsup|1>,m<rsup|1>|)>> and
    <math|<around*|(|u<rsup|2>,m<rsup|2>|)>>, we have 2 solutions for:

    <\equation*>
      \;
    </equation*>

    <\eqnarray*>
      <tformat|<table|<row|<cell|<big|int><rsub|0<rsup|>><rsup|T><big|int><around*|(|-\<partial\><rsub|t><around*|(|u<rsup|1>-u<rsub|><rsup|2>|)>-<frac|\<sigma\><rsup|2>|2>\<Delta\><around*|(|u<rsup|1>-u<rsup|2>|)>+<around*|(|H<around*|(|x,\<nabla\><rsub|x>u<rsup|1>|)>-H<around*|(|x,\<nabla\><rsub|x>u<rsup|2>|)>|)>|)>>|<cell|>|<cell|>>|<row|<cell|-<big|int><rsub|0<rsup|>><rsup|T><big|int><around*|(|f<around*|(|m<rsup|1>|)><around*|(|x|)>-f<around*|(|m<rsup|2>|)><around*|(|x|)>|)><around*|(|m<rsup|1>-m<rsup|2>|)>d
      x d t >|<cell|>|<cell|>>>>
    </eqnarray*>

    \;
  </proof>

  <section|Master equation>

  Suppose we have stochasticity on the evolution of the agents distribution.
  Thus, we have that <math|m> is an state itsfelt to the player (before,
  <math|m> was a function only of the time and the initial condition
  <math|m<rsub|0> >and thus its evolution was deterministic.) The new control
  problem reads

  <\equation*>
    U<around*|(|t,\<alpha\>,m|)>=inf<rsub|\<alpha\>> <with|font|Bbb|E>
    <around*|[|<big|int><rsub|0><rsup|T>L<around*|(|X<rsub|s>,\<alpha\><rsub|s>|)>+f<around*|(|m<rsub|s>|)><around*|(|X<rsub|>s|)>d
    s+G<around*|(|m<rsub|s>|)><around*|(|X<rsub|s>|)>|]>
  </equation*>

  with the dynamics for <math|X<rsub|s>>

  \;

  <\equation*>
    d X<rsub|s>=\<alpha\><rsub|s>d s+\<sigma\><rsup|>d W<rsub|s>
  </equation*>

  The master equation arises when the distribution of agents itself becomes
  stochastic and must be treated as part of the state of the control problem.
  In the classical mean field game formulation, the population distribution
  evolves deterministically once the initial distribution is fixed, and the
  value function depends only on time and the individual state. However, when
  randomness affects the evolution of the population \V for instance through
  common noise or stochastic aggregate shocks \V the distribution becomes a
  random object observed by the players. As a consequence, the value function
  must depend not only on time and the individual state but also on the
  current population distribution. The player therefore solves a control
  problem whose state variables are both the position of the agent and the
  distribution of the population.

  The derivation of the master equation follows from combining two
  ingredients. First, dynamic programming applied to the individual
  optimization problem yields a Hamilton\UJacobi\UBellman equation describing
  how the value function evolves along the agent's controlled stochastic
  dynamics. Second, the population distribution evolves according to a
  Fokker\UPlanck (or continuity) equation, which expresses conservation of
  mass under optimal motion and stochastic diffusion. Since the value
  function depends explicitly on the distribution, its time variation must
  account not only for changes in time and space but also for the
  infinitesimal change of the distribution itself. Applying a chain rule with
  respect to the measure argument introduces additional terms involving
  derivatives of the value function with respect to the distribution and the
  evolution law of the population.

  Substituting the evolution of the distribution given by the Fokker\UPlanck
  equation into the dynamic programming equation produces a single
  infinite-dimensional partial differential equation for the value function
  defined on time, space, and the space of probability measures. This
  equation is called the master equation. It encodes simultaneously the
  optimal behavior of an individual agent and the consistent evolution of the
  entire population, thereby replacing the coupled HJB\UFokker\UPlanck system
  with one unified equation. Conceptually, the master equation describes how
  the value of an agent changes when both its own state and the distribution
  of all agents evolve together under optimal responses and stochastic
  fluctuations.

  \;

  <subsection|Derivation of the Master equation.>

  <subsubsection|First method based on the Forward-Backwards system,>

  The HJB equation reads

  \;

  <\equation*>
    -\<partial\><rsub|t>U<around*|(|t,x,m|)>-<frac|\<sigma\><rsup|2>|2>\<Delta\><rsub|x>U<around*|(|t,x,m|)>+H<around*|(|\<alpha\>,\<nabla\>U<around*|(|t,x,m|)>|)>=f<around*|(|m|)><around*|(|x|)>
  </equation*>

  By chain rule, we have:

  <\equation*>
    <math|\<partial\><rsub|t>U<around*|(|t,x,m|)>>=\<partial\><rsub|t>U<around*|(|t,x,m|)>+<big|int><rsub|<with|font|Bbb|R>><frac|\<delta\>U|\<delta\>m><around*|(|t,x,m|)><around*|(|y|)>\<partial\><rsub|t>m<rsub|t><around*|(|y|)>dy
    </equation*>

  Thus we have

  \;

  <\equation*>
    <math|-\<partial\><rsub|t>U<around*|(|t,x,m|)>-<big|int><rsub|<with|font|Bbb|R>><frac|\<delta\>U|\<delta\>m><around*|(|t,x,m|)><around*|(|y|)>\<partial\><rsub|t>m<rsub|t><around*|(|y|)>dy-<frac|\<sigma\><rsup|2>|2>\<Delta\><rsub|x>U<around*|(|t,x,m|)>+H<around*|(|\<alpha\>,\<nabla\>U<around*|(|t,x,m|)>|)>=f<around*|(|m|)><around*|(|x|)>>
  </equation*>

  And using the definition of <math|\<partial\>m<rsub|t>>

  \;

  <\equation*>
    <big|int><rsub|<with|font|Bbb|R>><frac|\<delta\>U|\<delta\>m><around*|(|t,x,m|)><around*|(|y|)>\<partial\><rsub|t>m<rsub|t><around*|(|y|)>dy=<big|int><rsub|<with|font|Bbb|R>><frac|\<delta\>U|\<delta\>m><around*|(|t,x,m|)><around*|(|y|)><around*|(|div<around*|(|D<rsub|p>H<around*|(|y,\<nabla\><rsub|x>U|)>m|)>+<frac|\<sigma\><rsup|2>|2>\<Delta\>m|)><around*|(|y|)>dy
  </equation*>

  <math|<around*|(|D<rsub|p><rsub|>H|(>y,\<nabla\><rsub|x>U>

  \;

  <\eqnarray*>
    <tformat|<table|<row|<cell|<big|int><rsub|<with|font|Bbb|R>><frac|\<delta\>U|\<delta\>m><around*|(|t,x,m|)><around*|(|y|)>\<partial\><rsub|t>m<rsub|t><around*|(|y|)>dy>|<cell|=>|<cell|<around*|\<nobracket\>|<big|int><rsub|<with|font|Bbb|R>><frac|\<delta\>U|\<delta\>m><around*|(|t,x,m|)><around*|(|y|)><around*|(|div<around*|(|D<rsub|p><rsub|>H|(>y,\<nabla\><rsub|x>U|)>+<frac|\<sigma\><rsup|2>|2>\<Delta\>m|)><around*|(|y|)>dy>>|<row|<cell|>|<cell|=>|<cell|<frac|\<sigma\><rsup|2>|2><big|int><rsub|<with|font|Bbb|R>><frac|\<delta\>U|\<delta\>m><around*|(|y|)>\<Delta\>m<around*|(|y|)>dy+<big|int><rsub|<with|font|Bbb|R>><frac|\<delta\>U|\<delta\>m><around*|(|y|)><around*|(|div<around*|(|D<rsub|p><rsub|>H<around*|(|y,\<nabla\><rsub|x>U|)>
    m|)>|)><around*|(|y|)>dy>>>>
  </eqnarray*>

  Thus the equation reads:

  <\eqnarray*>
    <tformat|<table|<row|<cell|-\<partial\><rsub|t>U<around*|(|t,x,m|)>-<frac|\<sigma\><rsup|2>|2><big|int><rsub|<with|font|Bbb|R>><frac|\<delta\>U|\<delta\>m><around*|(|y|)>\<Delta\>m<around*|(|y|)>dy>|<cell|>|<cell|>>|<row|<cell|-<big|int><rsub|<with|font|Bbb|R>><frac|\<delta\>U|\<delta\>m><around*|(|y|)><around*|(|div<around*|(|D<rsub|p><rsub|><around*|(|\<nabla\><rsub|x>U|)>
    m|)>|)><around*|(|y|)>dy->|<cell|>|<cell|>>|<row|<cell|<frac|\<sigma\><rsup|2>|2>\<Delta\><rsub|x>U<around*|(|t,x,m|)>+H<around*|(|\<alpha\>,\<nabla\>U<around*|(|t,x,m|)>|)>=f<around*|(|m|)><around*|(|x|)>>|<cell|>|<cell|>>>>
  </eqnarray*>

  and we can re-write all by integration by parts<\footnote>
    We use the formulae for the transport and difussion parts:

    <\equation*>
      <big|int>\<phi\> div<around*|(|m b|)>=-<big|int>\<nabla\>\<phi\>\<cdot\>b
      m,<space|2em> <big|int>\<phi\>\<Delta\>m=<big|int>m\<Delta\>\<phi\>
    </equation*>

    \;

    \;
  </footnote>:

  \;

  \;
</body>

<\initial>
  <\collection>
    <associate|page-medium|paper>
    <associate|page-screen-margin|false>
  </collection>
</initial>

<\references>
  <\collection>
    <associate|auto-1|<tuple|1|5>>
    <associate|auto-10|<tuple|1|6>>
    <associate|auto-11|<tuple|2|6>>
    <associate|auto-12|<tuple|3|6>>
    <associate|auto-13|<tuple|4|6>>
    <associate|auto-14|<tuple|1.3|6>>
    <associate|auto-15|<tuple|2|9>>
    <associate|auto-16|<tuple|3|11>>
    <associate|auto-17|<tuple|3.1|?>>
    <associate|auto-18|<tuple|3.1.1|?>>
    <associate|auto-19|<tuple|3.1.2|?>>
    <associate|auto-2|<tuple|1.1|5>>
    <associate|auto-20|<tuple|3.1.3|?>>
    <associate|auto-21|<tuple|3.2|?>>
    <associate|auto-22|<tuple|3.2.1|?>>
    <associate|auto-23|<tuple|3.2.2|?>>
    <associate|auto-24|<tuple|3.3|?>>
    <associate|auto-25|<tuple|3.3.1|?>>
    <associate|auto-26|<tuple|3.3.1.1|?>>
    <associate|auto-3|<tuple|1|5>>
    <associate|auto-4|<tuple|2|5>>
    <associate|auto-5|<tuple|3|5>>
    <associate|auto-6|<tuple|4|5>>
    <associate|auto-7|<tuple|5|5>>
    <associate|auto-8|<tuple|6|6>>
    <associate|auto-9|<tuple|1.2|6>>
    <associate|footnote-3.1|<tuple|3.1|?>>
    <associate|footnote-3.2|<tuple|3.2|?>>
    <associate|footnr-3.1|<tuple|3.1|?>>
    <associate|footnr-3.2|<tuple|3.2|?>>
  </collection>
</references>

<\auxiliary>
  <\collection>
    <\associate|toc>
      <vspace*|1fn><with|font-series|<quote|bold>|math-font-series|<quote|bold>|font-shape|<quote|small-caps>|1.<space|2spc>Analysis
      in the space of measures> <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <pageref|auto-1><vspace|0.5fn>

      1.1.<space|2spc>Space of measures <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-2>

      <with|par-left|<quote|3tab>|Space <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-3>>

      <with|par-left|<quote|3tab>|Total variation of the set of measures.
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-4>>

      <with|par-left|<quote|3tab>|Action of functions.
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-5>>

      <with|par-left|<quote|3tab>|Couplings, disingetation and gluing.
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-6>>

      <with|par-left|<quote|3tab>|Wasserstein distance.
      \ <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-7>>

      <with|par-left|<quote|3tab>|Lifting.
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-8>>

      1.2.<space|2spc>variations <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-9>

      <with|par-left|<quote|3tab>|Linear variations.
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-10>>

      <with|par-left|<quote|3tab>|Action of flows ODE.
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-11>>

      <with|par-left|<quote|3tab>|Action of flows SDE.
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-12>>

      <with|par-left|<quote|3tab>|Following couple.
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-13>>

      1.3.<space|2spc>Derivative in the space of measure.
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-14>

      <vspace*|1fn><with|font-series|<quote|bold>|math-font-series|<quote|bold>|font-shape|<quote|small-caps>|2.<space|2spc>Mean
      field Control> <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <pageref|auto-15><vspace|0.5fn>

      <vspace*|1fn><with|font-series|<quote|bold>|math-font-series|<quote|bold>|font-shape|<quote|small-caps>|3.<space|2spc>Mean
      Field Games> <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <pageref|auto-16><vspace|0.5fn>
    </associate>
  </collection>
</auxiliary>