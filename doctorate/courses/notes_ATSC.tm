<TeXmacs|2.1.4>

<style|<tuple|tmbook|padded-paragraphs>>

<\body>
  <doc-data|<\doc-title>
    Argomenti avanzati

    di Calcolo Stocastico.
  </doc-title>>

  <chapter|>

  <subsection|Funzioni a variazione finita.>

  XXX

  <subsection|Processi a variazione finita.>

  Lavoriamo su uno spazio filtrato di probabalità completo
  <math|<around*|(|\<Omega\>,<with|font|cal|F>,<with|font|Bbb|P>|)>>.\ 

  <\definition>
    Un processo <math|<around*|(|X<rsub|t>|)><rsub|t\<geq\>0>=<inactive|<hybrid||<with|font-series|bold|X>>>>
    è detto a variazione finita (FV) se, q.c., le sue traiettorie sono a
    vrazione finita per ogni intervallo limitato. Aggiungiamo la condizione
    che siano continue.
  </definition>

  Perciò, fissato <math|\<omega\>>, q.c.,

  <\equation*>
    t \<mapsto\>X<rsub|t><around*|(|\<omega\>|)><space|1em>ha vrazione finita
    per ogni <around*|[|0,T|)>
  </equation*>

  Dato un processo <math|<around*|(|H<rsub|t>|)><rsub|t\<geq\>0>> se risulta
  q.c. che

  <\equation*>
    <big|int><rsub|0><rsup|T><around*|\||H<rsub|t><around*|(|\<omega\>|)>|\|>
    <around*|\||dX<rsub|t><around*|(|\<omega\>|)>|\|>\<less\>\<infty\>,<space|1em>\<forall\>T\<gtr\>0
  </equation*>

  allora è definito q.c.

  <\equation*>
    I<rsub|t><around*|(|\<omega\>|)>=<big|int><rsub|0><rsup|t>H<rsub|s><around*|(|\<omega\>|)>dX<rsub|s><around*|(|\<omega\>|)>,<space|1em>t\<geq\>0
  </equation*>

  <\note>
    Se <with|font-series|bold|X> è adattato allora è progressivo.
  </note>

  <\proposition>
    Sia <with|font-series|bold|X> adattato e FV, sia
    <with|font-series|bold|H> progressico. Se\ 

    <\equation*>
      <big|int><rsub|0><rsup|T><around*|\||H<rsub|s>|\|>
      <around*|\||dX<rsub|s>|\|>\<less\>\<infty\>,<space|1em>q.c.,<space|1em>\<forall\>T\<gtr\>0
    </equation*>

    Allora <math|\<b-I\>> è adattato (e quindi progressivo).
  </proposition>

  <\note>
    Notazione:

    <\equation*>
      I<rsub|t>=<big|int><rsub|0><rsup|t>H<rsub|s>dX<rsub|s>=<around*|(|H\<cdot\>X|)><rsub|t>
    </equation*>
  </note>

  cioè abbiamo che <math|<with|font-series|bold|I>=<with|font-series|bold|H>\<cdot\><with|font-series|bold|X>>.

  <\note>
    <math|<with|font-series|bold|H> progressivo e
    ><math|<big|int><rsub|0><rsup|T><around*|\||H<rsub|s>|\|>
    <around*|\||dX<rsub|s>|\|>\<less\>\<infty\>,><math|<with|font-series|bold|X>>
    a FV. Allora abbiamo che <math|<with|font-series|bold|H>\<cdot\><with|font-series|bold|X>>
    è FV progressivo.\ 
  </note>

  Dato un processo <math|<with|font-series|bold|K>> progressivo posso
  definite

  <\equation*>
    <with|font-series|bold|K>\<cdot\><around*|(|<with|font-series|bold|H>\<cdot\><with|font-series|bold|X>|)>=<with|font-series|bold|K>\<cdot\><with|font-series|bold|I>
  </equation*>

  a condizione\ 

  <\equation*>
    <big|int><rsub|0><rsup|T><around*|\||K<rsub|s>|\|>
    <around*|\||dI<rsub|s>|\|>\<less\>\<infty\>
  </equation*>

  <\proposition>
    I processi <with|font-series|bold|H> e <with|font-series|bold|K> sono
    progressivi e

    <\equation*>
      <big|int><rsub|0><rsup|T><around*|\||K<rsub|s>|\|>
      <around*|\||dX<rsub|s>|\|>\<less\>\<infty\>,<space|1em><big|int><rsub|0><rsup|T><around*|\||H<rsub|s>K<rsub|s>|\|>
      <around*|\||dX<rsub|s>|\|>\<less\>\<infty\>,<space|1em>q.c.,<space|1em>
      \<forall\>T\<gtr\>0
    </equation*>
  </proposition>

  Allora abbiamo

  <\equation*>
    <with|font-series|bold|K>\<cdot\><around*|(|<with|font-series|bold|H>\<cdot\><with|font-series|bold|X>|)>=<with|font-series|bold|K><with|font-series|bold|H>\<cdot\><with|font-series|bold|X>
  </equation*>

  cioè\ 

  <\equation*>
    <big|int><rsub|0><rsup|t >K<rsub|s ><text|d><around*|(|<big|int><rsub|0><rsup|s>H<rsub|u>dX<rsub|u>|)>=<big|int><rsub|0><rsup|t>K<rsub|s>H<rsub|s>dX<rsub|s>
  </equation*>

  \;

  Ricordiamo che:

  <\enumerate-Roman>
    <item><math|<with|font|cal|M><rsub|loc><rsup|c>>: sono le martingali
    locali continue

    <item>FV: sono processi adattati con traiettorie continue a variazione
    finita.
  </enumerate-Roman>

  Risulta che <math|><math|<with|font|cal|M><rsub|loc><rsup|c> <big|cap>>FV =
  <math|<around*|{|processo nullo|}>>. Infatti Abbiamo che

  <\theorem>
    <with|font-series|bold|M> \<in\> <math|<with|font|cal|M><rsub|loc><rsup|c>>,
    <math|M<rsub|0>=0. Se ><with|font-series|bold|M> ha una traiettoria q.c.
    a varazione finita, allora abbiamo che <math|M<rsub|0>=0 > (cioè è
    indistinguibile dal processo nullo).\ 
  </theorem>

  <\lemma>
    <with|font-series|bold|M> è una martingala in <math|L<rsup|2>>. Se
    <math|0\<leq\>s\<leq\>t> allora <math|<with|font|Bbb|E><around*|[|M<rsub|t><rsup|2>-M<rsub|s><rsup|2>|]>=><with|font|Bbb|<math|>><math|<with|font|Bbb|E><around*|[|<around*|(|M<rsub|t><rsup|>-M<rsub|s><rsup|>|)><rsup|2>|]>>.
  </lemma>

  <\proof>
    Abbiamo

    <\eqnarray*>
      <tformat|<table|<row|<cell|<around*|(|M<rsub|t><rsup|>-M<rsub|s><rsup|>|)><rsup|2>>|<cell|=>|<cell|M<rsub|t<rsup|>><rsup|2>+M<rsub|s><rsup|2>-2M<rsub|s
      >M<rsub|t>>>|<row|<cell|>|<cell|=>|<cell|M<rsub|t<rsup|>><rsup|2>-M<rsub|s><rsup|2>-2M<rsub|s
      ><around*|(|M<rsub|t>-M<rsub|s>|)>>>>>
    </eqnarray*>

    Allora

    <\equation*>
      <with|font|Bbb|E><around*|[|M<rsub|s><around*|(|M<rsub|t>-M<rsub|s>|)><around*|\||<with|font|cal|F<rsub|>><rsub|s>|\<nobracket\>>|]>=M<rsub|s><with|font|Bbb|E><around*|[|<around*|(|M<rsub|t>-M<rsub|s>|)><around*|\||<with|font|cal|F<rsub|>><rsub|s>|\<nobracket\>>|]>=0\<Rightarrow\><with|font|Bbb|E><around*|[|M<rsub|s><around*|(|M<rsub|t>-M<rsub|s>|)>|]>=0
    </equation*>

    \;
  </proof>

  \;

  <\proof>
    <dueto|del teorema>Sia <with|font-series|bold|M> a variazione limitata da
    <math|K\<gtr\>0>:

    <\equation*>
      <around*|\||V<rsub|t><rsup|M><around*|(|\<omega\>|)>|\|>\<leq\>K
      <with|color|red|<around*|(|\<Rightarrow\><around*|\||M<rsub|t><around*|(|\<omega\>|)>|\|>\<leq\>K
      \<Rightarrow\>M martingala vera.|)>>
    </equation*>

    \;

    Fisso e considero la partizione <math|\<pi\>=<around*|{|0=t<rsub|0>\<less\>t<rsub|1>
    ...\<less\>t<rsub|n>=t|}>> e allora

    <\equation*>
      M<rsub|t><rsup|2>=<around*|(|M<rsub|t<rsub|n>><rsup|2>-M<rsub|t<rsub|n-1>><rsup|2>|)>+<around*|(|M<rsub|t<rsub|n-1><rsup|>><rsup|2>-M<rsub|t<rsub|n-2><rsup|>><rsup|2>|)>+<around*|(|\<ldots\>|)>+<around*|(|M<rsub|t<rsub|1>><rsup|2>-<wide*|M<rsub|t<rsub|0>><rsup|2>|\<wide-underbrace\>><rsub|=0>|)>=<rsub|><big|sum><rsub|i=1><rsup|n><around*|(|M<rsub|t<rsub|i>><rsup|2>-M<rsub|t<rsub|i-1>><rsup|2>|)>
    </equation*>

    E allora\ 

    <\eqnarray*>
      <tformat|<table|<row|<cell|<with|font|Bbb|E><around*|[|M<rsub|t><rsup|2>|]>>|<cell|=>|<cell|<big|sum><rsub|i=1><rsup|n><with|font|Bbb|E><around*|[|M<rsub|t<rsub|i>><rsup|2>-M<rsub|t<rsub|i-1>><rsup|2>|]>>>|<row|<cell|>|<cell|=>|<cell|<big|sum><rsub|i=1><rsup|n><with|font|Bbb|E><around*|[|<around*|(|M<rsub|t<rsub|i>><rsup|>-M<rsub|t<rsub|i-1>><rsup|>|)><rsup|2>|]>>>|<row|<cell|>|<cell|=>|<cell|<with|font|Bbb|E>
      <around*|[|<big|sum><rsub|i=1><rsup|n><with|font|Bbb|><around*|(|M<rsub|t<rsub|i>><rsup|>-M<rsub|t<rsub|i-1>><rsup|>|)><rsup|2>|]><rsup|>
      >>|<row|<cell|>|<cell|\<leq\>>|<cell|<with|font|Bbb|E><around*|[|sup<rsub|i><around*|\||M<rsub|t<rsub|i>><rsup|>-M<rsub|t<rsub|i-1>><rsup|>|\|>
      <big|sum><rsub|i=1><rsup|n><around*|\||M<rsub|t<rsub|i>><rsup|2>-M<rsub|t<rsub|i-1>><rsup|2>|\|>
      |]>>>|<row|<cell|>|<cell|\<leq\>>|<cell|<with|font|Bbb|E><around*|[|sup<rsub|i><around*|\||M<rsub|t<rsub|i>><rsup|>-M<rsub|t<rsub|i-1>><rsup|>|\|>
      V<rsub|t><rsup|M> |]>>>|<row|<cell|>|<cell|\<leq\>>|<cell|<wide*|K
      <with|font|Bbb|E><around*|[|<wide*|sup<rsub|i><around*|\||M<rsub|t<rsub|i>><rsup|>-M<rsub|t<rsub|i-1>><rsup|>|\|>|\<wide-underbrace\>><rsub|\<rightarrow\>0<space|1em>q.c.
      \ se \ diam<around*|(|\<pi\>|)>\<rightarrow\>0>
      |]>\<rightarrow\><rsub|>0|\<wide-underbrace\>><rsub|per convergenza
      dominata.> >>>>
    </eqnarray*>

    E abbiamo che <math|<with|font|Bbb|E><around*|[|M<rsub|t><rsup|2>|]>=0> e
    per ogni <math|t >abbiamo <math|M<rsub|t>=0 > q.c. e
    <with|font-series|bold|M> è conitno <math|\<Rightarrow\><with|font-series|bold|M>=0>
    indistiguinbile.

    Nel caso generale definiamo

    <\equation*>
      T<rsub|n>=inf<around*|{|t\<geq\>0:V<rsub|t><rsup|M>\<geq\>n|}>
    </equation*>

    e allora <math|<around*|(|V<rsup|M>|)><rsub|t><rsup|T<rsub|n>>=V<rsub|t\<wedge\>T<rsub|n>><rsup|M>\<leq\>n
    > <math|\<Rightarrow\><with|font-series|bold|M><rsup|T<rsub|n>>> ha
    variazione limiata da <math|n>. Per quanto dimostrato,
    <math|<with|font-series|bold|M><rsup|T<rsub|n>>=0,cioè q.c. abbiamo che
    M<rsub|t\<wedge\>T<rsub|n>>=0> per ogni <math|t> e per
    <math|n\<rightarrow\>0>, <math|M<rsub|t>=0> per ogni <math|t>, cioè
    <math|<with|font-series|bold|M>=0.>
  </proof>

  <subsection|Martingale locali continue.>

  <\definition>
    Sia <math|<with|font-series|bold|M>> un processo continuoa adattao.
    Allora

    <\enumerate-roman>
      <item>Sia <math|M<rsub|0>=0. Il processo <with|font-series|bold|M> è
      detto martingala locale continua se esitono T<rsup|n>> tempi di arresto
      tali che <math|<with|font-series|bold|M><rsup|T<rsub|n>>> sono
      martingale UI e <math|T<rsup|n> \<uparrow\>> \<infty\> q.c.

      <item>In generale, <math|<with|font-series|bold|M>> è detto martingale
      locale continua se <math|<around*|(|M<rsub|t>-M<rsub|0>|)><rsub|t\<geq\>0>>
      è martingalr locale continua come definita sopra.
    </enumerate-roman>
  </definition>

  <\note>
    Ogni processo indistiguibile de <math|<with|font-series|bold|M > è detto
    martingale locale continua.>
  </note>

  <\note>
    Notazione, <math|M\<in\> <with|font|cal|M><rsub|loc><rsup|c> e
    ><math|<with|font|cal|M><rsub|loc,0><rsup|c> se M<rsub|0>=0.
    Terminologia,diciamo che ><math|T<rsup|n> ><em|riduce>
    <math|<with|font-series|bold|M>.>
  </note>

  <\remark>
    Abbiamo le seguenti osservazioni:

    <\enumerate-roman>
      <item><with|font-series|bold|<math|M>> è una martingala continua allora
      <with|font-series|bold|><math|<with|font-series|bold|M>\<in\>
      <with|font|cal|M><rsub|loc><rsup|c>. >

      <with|color|red|<em|Infatti sia <math|M<rsub|0>=0>. Scelgo
      <math|T<rsub|><rsup|n>=n> e <math|M<rsub|t><rsup|T<rsub|><rsup|n>>=><math|M<rsub|t\<wedge\>n><rsup|>>
      è martingale ed è U.I>>

      <item><math|M<rsub|0>=0>. \ <math|T<rsub|><rsup|n>> riduce
      <math|<with|font-series|bold|M>> e se <math|S<rsup|n> >sono tempi dia
      rresto con <math|S<rsup|n> \<uparrow\> \<infty\>> q.c. allora
      \ <math|T<rsub|><rsup|n>>\<wedge\><math|S<rsup|n>> riduce
      <math|<with|font-series|bold|M >>

      <with|color|red|<\em>
        Infatti,\ 

        <\equation*>
          <with|font-series|bold|M><rsup|T<rsup|n>\<wedge\>S<rsup|n>>=<around*|(|<wide*|<with|font-series|bold|M><rsup|T<rsup|n>><rsub|><rsup|>|\<wide-underbrace\>><rsub|martingala<space|1em>UI>|)><rsup|S<rsup|n>><rsup|>
        </equation*>

        è martingala UI e <math|T<rsub|><rsup|n>>\<wedge\><math|S<rsup|n>
        \<uparrow\>>\<infty\> q.c.
      </em>>

      <item>Se <with|font-series|bold|<math|M>> è continuo adattato,
      <math|M<rsub|0>=0,> <math|T<rsup|n>> tale che \ <math|T<rsup|n >
      \<uparrow\> \<infty\>> q.c. e <math|<with|font-series|bold|M><rsup|T<rsup|n>><rsub|><rsup|>>
      è una martingala (non necesseriamente UI). Allora abbiamo che
      <math|<with|font-series|bold|M>\<in\>
      <with|font|cal|M><rsub|loc><rsup|c>. >

      <\em>
        <\with|color|red>
          Infatti, considero <math|T<rsup|n >\<wedge\>n> e abbiamo\ 

          <\equation*>
            <with|font-series|bold|M><rsup|T<rsup|n>\<wedge\>n>=<around*|(|<wide*|<with|font-series|bold|M><rsup|n>|\<wide-underbrace\>><rsub|è
            \ m. UI. M<rsub|t><rsup|n>=M<rsub|t\<wedge\>n>>|)><rsup|T<rsup|n>>
          </equation*>
        </with>

        è martingala UI e quindi \ <math|T<rsup|n >\<wedge\>n> riduce
        <with|font-series|bold|M> e allora abbiamo
        <math|<with|font-series|bold|M>\<in\>
        <with|font|cal|M><rsub|loc><rsup|c>.>
      </em>

      <item><math|<with|font-series|bold|M>\<in\>
      <with|font|cal|M><rsub|loc><rsup|c>> e <math|T> è un tempo di arresto
      \<Rightarrow\><math|<with|font-series|bold|M><rsup|T >\<in\>
      <with|font|cal|M><rsub|loc><rsup|c>>.

      <with|color|red|<\em>
        Infatti sia <math|M<rsub|0>=0. Se T<rsub|n>> riduce
        <with|font-series|bold|M> allora\ 

        <\equation*>
          <around*|(|<with|font-series|bold|M><rsup|T>|)><rsup|T<rsup|n>>=M<rsup|T\<wedge\>T<rsup|n>>=<around*|(|<wide*|M<rsup|T<rsup|n>>|\<wide-underbrace\>><rsub|è
          martingala UI>|)><rsup|T> è martingala UI.
        </equation*>

        \;
      </em>>

      \;
    </enumerate-roman>
  </remark>

  <\remark>
    <math|<with|font|cal|M><rsub|loc><rsup|c> e
    <with|font|cal|M><rsub|loc,0><rsup|c>> sono spazi vettoriali.

    <\remark>
      Se <math|<with|font-series|bold|M>\<in\>
      <with|font|cal|M><rsub|loc><rsup|c> > e
      <math|<with|font-series|bold|M>> è una martingala UI allora questo non
      implica che <math|<with|font-series|bold|M>> sia una martingala.
    </remark>
  </remark>

  <\proposition>
    Sia <math|<with|font-series|bold|M>\<in\>
    ><math|<with|font|cal|M><rsub|loc><rsup|c>>

    <\enumerate-roman>
      <item>Se <math|M<rsub|t>\<geq\>0> for all t\<geq\>0,
      <math|M<rsub|0>\<in\> L<rsup|1>> allora <with|font-series|bold|M> è una
      sopra-martingala.

      <item>Se, q.c., <math|<around*|\||M<rsub|t>|\|>\<leq\>Z<rsub|t>> for
      all t\<geq\>0, Z \<in\> <math|L<rsup|1>> allora
      <with|font-series|bold|M> è una martingala UI.

      <item>Sia <math|M<rsub|0>=0> e definiaimo
      <math|T<rsup|n>=inf<around*|{|t\<geq\>0:<around*|\||M<rsub|t>|\|>\<geq\>n|}>.>
      Allora <math|T<rsup|n>> riduce <with|font-series|bold|M> e
      <math|<around*|\||M<rsub|t><rsup|T<rsup|n>>|\|>\<leq\>n
      <prefix-for-all>t.>
    </enumerate-roman>
  </proposition>

  <\proof>
    \;

    <\enumerate-roman>
      <item><math|N<rsub|t>=M<rsub|t>-M<rsub|0>> e <math|N<rsub|t>\<in\>
      ><math|<with|font|cal|M><rsub|loc,0><rsup|c>.> Prendiamo un tempo di
      arresto <math|T<rsup|n>> che riduce <math|<with|font-series|bold|N>>,
      cioè <math|<with|font-series|bold|N><rsup|T<rsub|n> >> è una martingala
      UI. Se <math|0\<leq\>s\<leq\>t, abbiamo>

      <\eqnarray*>
        <tformat|<table|<row|<cell|N<rsub|T<rsup|n>\<wedge\>s>>|<cell|=>|<cell|<with|font|Bbb|E><around*|[|N<rsub|T<rsup|n>\<wedge\>t><around*|\||<with|font|cal|F<rsub|>>|\<nobracket\>><rsub|s>|]>>>|<row|<cell|N<rsub|T<rsup|n>\<wedge\>s>+M<rsub|0>>|<cell|=>|<cell|<with|font|Bbb|E><around*|[|N<rsub|T<rsup|n>\<wedge\>t>+M<rsub|0><around*|\||<with|font|cal|F<rsub|>>|\<nobracket\>><rsub|s>|]>>>|<row|<cell|M<rsub|T<rsup|n>\<wedge\>s>>|<cell|=>|<cell|<with|font|Bbb|E><around*|[|M<rsub|T<rsup|n>\<wedge\>t><around*|\||<with|font|cal|F<rsub|>>|\<nobracket\>><rsub|s>|]>>>>>
      </eqnarray*>

      e vediamo <math|n\<rightarrow\>\<infty\>,><math|M<rsub|T<rsup|n>\<wedge\>s>\<rightarrow\>M<rsub|s>,><math|M<rsub|T<rsup|n>\<wedge\>t>\<rightarrow\>M<rsub|t>>
      q.c. allora per Fatou condizionale

      <\equation*>
        <tabular|<tformat|<table|<row|<cell|<with|font|Bbb|E><around*|[|M<rsub|t><around*|\||<with|font|cal|F<rsub|>>|\<nobracket\>><rsub|s>|]>>|<cell|=>|<cell|<with|font|Bbb|E><around*|[|lim
        inf M<rsub|t\<wedge\>T<rsup|n>><around*|\||<with|font|cal|F<rsub|>>|\<nobracket\>><rsub|s>|]>>>|<row|<cell|>|<cell|\<leq\>>|<cell|lim
        inf <with|font|Bbb|E><around*|[|M<rsub|t\<wedge\>T<rsup|n>><around*|\||<with|font|cal|F<rsub|>>|\<nobracket\>><rsub|s>|]>>>|<row|<cell|>|<cell|=>|<cell|lim
        inf <with|font|Bbb|>M<rsub|s\<wedge\>T<rsup|n>>=M<rsub|s>>>>>>
      </equation*>

      e consideriamo <math|s=0>,\ 

      <\eqnarray*>
        <tformat|<table|<row|<cell|<with|font|Bbb|E><around*|[|M<rsub|t><around*|\||<with|font|cal|F<rsub|>>|\<nobracket\>><rsub|0>|]>>|<cell|\<leq\>>|<cell|M<rsub|0>>>|<row|<cell|<with|font|Bbb|E><around*|[|M<rsub|t>|]>>|<cell|\<leq\>>|<cell|<with|font|Bbb|E><around*|[|M<rsub|0>|]>\<in\>
        L<rsup|2>>>>>
      </eqnarray*>

      e allora <math|><with|font-series|bold|<math|M>> è una sopramartingala.

      <item>Come prima, abbiamo

      <\equation*>
        <tabular|<tformat|<table|<row|<cell|M<rsub|T<rsup|n>\<wedge\>s>>|<cell|=>|<cell|<with|font|Bbb|E><around*|[|M<rsub|T<rsup|n>\<wedge\>t><around*|\||<with|font|cal|F<rsub|>>|\<nobracket\>><rsub|s>|]>>>>>>
      </equation*>

      <math|M<rsub|T<rsup|n>\<wedge\>s>\<rightarrow\>M<rsub|s>,><math|M<rsub|T<rsup|n>\<wedge\>t>\<rightarrow\>M<rsub|t>>
      \ q.c. Abbiamo

      <\equation*>
        <around*|\||M<rsub|T<rsup|n>\<wedge\>t>|\|>\<leq\>Z,M<rsub|T<rsup|n>\<wedge\>t>\<rightarrow\>M<rsub|t>\<in\>
        L<rsup|1>\ 
      </equation*>

      e possiamo passare al limite, ottenendo\ 

      <\equation*>
        <tabular|<tformat|<table|<row|<cell|M<rsub|s>>|<cell|=>|<cell|<with|font|Bbb|E><around*|[|M<rsub|t><around*|\||<with|font|cal|F<rsub|>>|\<nobracket\>><rsub|s>|]>>>>>>
      </equation*>

      <item>Abbiamo che <math|M<rsub|t><rsup|T<rsup|n>>\<leq\>n>. Mostro che
      <math|M<rsub|t><rsup|T<rsup|n>>>è una martingala e se <math|S<rsup|n>>
      riduce <with|font-series|bold|M>:

      <\equation*>
        <around*|(|M<rsup|T<rsup|n>>|)><rsup|S<rsup|n>>=<around*|(|<wide*|M<rsup|S<rsup|n>>|\<wide-underbrace\>><rsub|martingala
        UI.>|)><rsup|T<rsup|n>>è una martingala UI.
      </equation*>

      \;
    </enumerate-roman>

    \;
  </proof>

  <subsection|Variazione quadratica delle martingali locali continue.>

  <\theorem>
    <with|font-series|bold|M> \<in\> <math|<with|font|cal|M><rsub|loc><rsup|c>.>
    Esiste un unico processo, indicato <math|<around*|\<langle\>|<with|font-series|bold|M>,<with|font-series|bold|M>|\<rangle\>>>,
    crescente, continuo, adattato e nullo in <math|t=0> tale che

    <\equation*>
      <with|font-series|bold|M><rsup|2>-<around*|\<langle\>|<with|font-series|bold|M>,<with|font-series|bold|M>|\<rangle\>>\<in\>
      <with|font|cal|M><rsub|loc><rsup|c>.
    </equation*>

    <math|<around*|\<langle\>|<with|font-series|bold|M>,<with|font-series|bold|M>|\<rangle\>>
    è detto la variazione quadratica di <with|font-series|bold|M>. > Dato
    <math|t\<gtr\>0> e consideriamo la partizione
    <math|\<Pi\><rsup|n>=<around*|{|0=t<rsub|0><rsup|n>\<less\>\<cdots\>\<less\>t<rsup|n><rsub|p<rsup|n>>=t|}>>
    con diam<math|(<math|\<Pi\><rsup|n>>)>=
    max<math|<around*|(|t<rsub|i><rsup|n>-t<rsub|i-1><rsup|n>|)>>\<rightarrow\>0
    e abbiamo

    <\equation*>
      <big|sum><rsub|i=1><rsup|p<rsup|n>><around*|(|M<rsub|t<rsub|i><rsup|n>>-M<rsub|t<rsub|i><rsup|n>-1>|)><rsup|2>\<longrightarrow\><rsup|><around*|\<langle\>|M,M<with|font-series|bold|>|\<rangle\>><rsub|t><space|1em>in
      probabilità.
    </equation*>
  </theorem>

  <\remark>
    <math|<around*|\<langle\>|<with|font-series|bold|M>,<with|font-series|bold|M>|\<rangle\>>
    non dipende da M<rsub|0>.>
  </remark>

  <\remark>
    <math|<around*|\<langle\>|<with|font-series|bold|M>,<with|font-series|bold|M>|\<rangle\>>
    è unicito <around*|(|up to indistiguibility|)>.> Se
    <math|<with|font-series|bold|A>> è adattato, continuo,
    <math|A<rsub|0>=0>, e abbiamo che <math|(<math|<with|font-series|bold|M><rsup|2>-><with|font-series|bold|A>)<math|\<in\><math|<with|font|cal|M><rsub|loc><rsup|c>>
    >> e allora

    <\equation*>
      <math|<with|font-series|bold|M><rsup|2>-><with|font-series|bold|A>-<around*|(|<math|<with|font-series|bold|M><rsup|2>-><with|font-series|bold|<around*|\<langle\>|<with|font-series|bold|M>,<with|font-series|bold|M>|\<rangle\>>>|)>\<in\>
      <with|font|cal|M><rsub|loc><rsup|c>
    </equation*>

    cioè <math|<wide*|<math|<with|font-series|bold|A->><math|<around*|\<langle\>|<with|font-series|bold|M>,<with|font-series|bold|M>|\<rangle\>>>|\<wide-underbrace\>><rsub|FV>\<in\>
    <math|<with|font|cal|M><rsub|loc><rsup|c>>> e allora
    <math|<math|<with|font-series|bold|A>=><math|<around*|\<langle\>|<with|font-series|bold|M>,<with|font-series|bold|M>|\<rangle\>>>>
    up to indistuinguibility.
  </remark>

  <\proposition>
    <with|font-series|bold|M> <math|\<in\>
    <math|<with|font|cal|M><rsub|loc><rsup|c>>> e T è un tempo di arresto.
    Allora

    <\equation*>
      <around*|\<langle\>|<with|font-series|bold|M><rsup|T>,<with|font-series|bold|M><rsup|T>|\<rangle\>>=<around*|\<langle\>|<with|font-series|bold|M><rsup|>,<with|font-series|bold|M>|\<rangle\>><rsup|T>
    </equation*>
  </proposition>

  <\proof>
    Consideriamo\ 

    <\eqnarray*>
      <tformat|<table|<row|<cell|<with|font-series|bold|M><rsup|2>-<around*|\<langle\>|<with|font-series|bold|M>,<with|font-series|bold|M>|\<rangle\>>>|<cell|\<in\>
      >|<cell|<with|font|cal|M><rsub|loc><rsup|c>>>|<row|<cell|<around*|(|<with|font-series|bold|M><rsup|2>-<around*|\<langle\>|<with|font-series|bold|M>,<with|font-series|bold|M>|\<rangle\>>|)><rsup|T>>|<cell|\<in\>
      >|<cell|<with|font|cal|M><rsub|loc><rsup|c>>>|<row|<cell|<around*|(|<with|font-series|bold|M><rsup|T>|)><rsup|2>-<around*|\<langle\>|<with|font-series|bold|M>,<with|font-series|bold|M>|\<rangle\>><rsup|T>>|<cell|\<in\>
      >|<cell|<with|font|cal|M><rsub|loc><rsup|c>>>>>
    </eqnarray*>

    e per definizion, <math|<around*|\<langle\>|<with|font-series|bold|M>,<with|font-series|bold|M>|\<rangle\>><rsup|T>>
    è la variazione quadratica di <math|<with|font-series|bold|M>><math|<rsup|T>.>
  </proof>

  <\proposition>
    <with|font-series|bold|M> <math|\<in\>
    <math|<with|font|cal|M><rsub|loc><rsup|c>>>, <math|M<rsub|0>=0. Allora>

    <\equation*>
      <with|font-series|bold|M>=0 \<Leftrightarrow\><around*|\<langle\>|<with|font-series|bold|M>,<with|font-series|bold|M>|\<rangle\>><rsup|>=0.
    </equation*>
  </proposition>

  <\proof>
    <math|<with|font-series|bold|M><rsup|2>=<with|font-series|bold|M><rsup|2>-<around*|\<langle\>|<with|font-series|bold|M>,<with|font-series|bold|M>|\<rangle\>>
    >è una martingala locale. Abbiamo che
    <math|><math|<with|font-series|bold|M><rsup|2>\<geq\>0> e
    <math|<with|font-series|bold|<math|>>><math|<math|<with|font-series|bold|M><rsup|2>>\<in\><math|<with|font|cal|M><rsub|loc><rsup|c>
    > >e allora

    <math|<with|font-series|bold|M><rsup|2> è> sottomartingala. Abbiamo\ 

    <\equation*>
      <with|font|Bbb|E><around*|[|M<rsub|t><rsup|2>|]>\<leq\><with|font|Bbb|E><around*|[|M<rsub|0><rsup|2>|]>=0
    </equation*>

    e per ogni <math|t>, <math|M<rsub|t>=0> q.c. e
    <with|font-series|bold|<math|M>> continua abbiamo che
    <math|<with|font-series|bold|M>=0.>

    \;
  </proof>

  <\remark>
    <math|<around*|\<langle\>|M,M|\<rangle\>><rsub|\<infty\>>=><math|lim<rsub|t\<rightarrow\>\<infty\>>>
    <math|<around*|\<langle\>|M,M|\<rangle\>><rsub|t>>
  </remark>

  <\proposition>
    <with|font-series|bold|M> <math|\<in\>
    <math|<with|font|cal|M><rsub|loc><rsup|c>>>, <math|M<rsub|0>\<in\>
    L<rsup|2>:>

    <\enumerate-roman>
      <item><with|font-series|bold|M> è una martingala limitata in
      <math|L<rsup|2>> \<Rightarrow\> <math|<with|font|Bbb|E><around*|[|<around*|\<langle\>|M,M|\<rangle\>><rsub|\<infty\>>|]>\<less\>\<infty\>>

      <with|color|red|<math|<around*|(|cioè sup<rsub|t>
      <with|font|Bbb|E><around*|[|<around*|\||M<rsub|t>|\|><rsup|2>|]>\<less\>\<infty\>|)>>>

      In tal caso, <math|<with|font-series|bold|M><rsup|2>-<around*|\<langle\>|<with|font-series|bold|M>,<with|font-series|bold|M>|\<rangle\>>>
      è una martingala UI.

      <item><with|font-series|bold|M> è una martingala in <math|L<rsup|2>>
      \<Rightarrow\> <math|<with|font|Bbb|E><around*|[|<around*|\<langle\>|M,M|\<rangle\>><rsub|t>|]>\<less\>\<infty\>>
      \<forall\>t\<geq\>0

      <with|color|red|<math|<around*|(|cioè
      \ <with|font|Bbb|E><around*|[|<around*|\||M<rsub|t>|\|><rsup|2>|]>\<less\>\<infty\>,\<forall\>t\<geq\>0|)>>>

      In tal caso, <math|<with|font-series|bold|M><rsup|2>-<around*|\<langle\>|<with|font-series|bold|M>,<with|font-series|bold|M>|\<rangle\>>>
      è una martingala.
    </enumerate-roman>
  </proposition>

  <\proof>
    \;
  </proof>

  <\remark>
    Se <with|font-series|bold|<math|M>> è una martingala locale continua e
    <math|<with|font-series|bold|M>> è una martingala lmitata in
    <math|L<rsup|2>>, questo non implica che <with|font-series|bold|<math|M>>
    sia una martingal o che <math|<with|font|Bbb|E><around*|[|<around*|\<langle\>|M,M|\<rangle\>><rsub|\<infty\>>|]>\<less\>\<infty\>>.
  </remark>

  Consideriamo <math|<with|font-series|bold|N>,<with|font-series|bold|M>
  <math|\<in\> <math|<with|font|cal|M><rsub|loc><rsup|c>>>>. Ricordiamo che
  <math|ab=<frac|1|2><around*|(|a+b|)><rsup|2>-a<rsup|2>-b<rsup|2>>. Ora
  definiamo la variazione quadratica congiunta.

  <\equation*>
    <around*|\<langle\>|<with|font-series|bold|M>,<with|font-series|bold|N>|\<rangle\>>=<frac|1|2><around*|\<langle\>|<with|font-series|bold|M>+<with|font-series|bold|N>,<with|font-series|bold|<with|font-series|bold|M>>+<with|font-series|bold|N>|\<rangle\>>-<around*|\<langle\>|<with|font-series|bold|M>,<with|font-series|bold|M>|\<rangle\>>-<around*|\<langle\>|<with|font-series|bold|N>,<with|font-series|bold|N>|\<rangle\>>
  </equation*>

  <\remark>
    <math|<around*|\<langle\>|<with|font-series|bold|M>,<with|font-series|bold|N>|\<rangle\>>>
    è a variazione finita.

    <\proposition>
      Abbiamo le seguenti proprietà:

      <\enumerate-roman>
        <item><math|<around*|\<langle\>|<with|font-series|bold|M>,<with|font-series|bold|N>|\<rangle\>>>
        è l'unico processo a variazione finita tale che\ 

        <\equation*>
          <with|font-series|bold|M><with|font-series|bold|N>-<around*|\<langle\>|<with|font-series|bold|M>,<with|font-series|bold|N>|\<rangle\>>\<in\>
          <math|<with|font|cal|M><rsub|loc><rsup|c>>
        </equation*>

        <item>Per <math|\<Pi\>=<around*|{|0=t<rsub|0>\<less\>\<cdots\>\<less\>t<rsub|n>=t|}>>
        e abbiamo per <math|<around*|\||\<Pi\>|\|>\<rightarrow\>0>

        <\equation*>
          <big|sum><rsub|i=1><rsup|n><around*|(|M<rsub|t<rsup|i>>-M<rsub|t<rsup|i>-1>|)><around*|(|N<rsub|t<rsup|i>>-N<rsub|t<rsup|i>-1>|)>\<longrightarrow\><around*|\<langle\>|M,N|\<rangle\>><rsub|t>
          in probabilità.
        </equation*>

        <item><math|<around*|\<langle\>|<with|font-series|bold|M><rsup|T>,<with|font-series|bold|N><rsup|T>|\<rangle\>>=><math|<around*|\<langle\>|<with|font-series|bold|M><rsup|T>,<with|font-series|bold|N><rsup|>|\<rangle\>>=<around*|\<langle\>|<with|font-series|bold|M><rsup|>,<with|font-series|bold|N>|\<rangle\>><rsup|T>>

        <item><math|<around*|(|<with|font-series|bold|M><rsup|>,<with|font-series|bold|N>|)>
        \<mapsto\>><math|<around*|\<langle\>|<with|font-series|bold|M><rsup|>,<with|font-series|bold|N>|\<rangle\>>>
        è simmetrica e bilineare.

        <item>Se <math|<with|font-series|bold|M><rsup|>,<with|font-series|bold|N>>
        sono martingale limiate in <math|L<rsup|2>> allora
        <math|<with|font-series|bold|M><with|font-series|bold|N>-<around*|\<langle\>|<with|font-series|bold|M>,<with|font-series|bold|N>|\<rangle\>>>
        è martingala UI.
      </enumerate-roman>
    </proposition>
  </remark>

  <\definition>
    <dueto|Semimartingala>Una semimartingala continua è\ 

    <\equation*>
      <with|font-series|bold|X>=<with|font-series|bold|M>+<with|font-series|bold|A>
    </equation*>

    dove <math|<with|font-series|bold|M> <math|\<in\>
    <math|<with|font|cal|M><rsub|loc><rsup|c>>>> e <with|font-series|bold|A>
    è un processo a variazione finita (con <math|A<rsub|0>=0>).
  </definition>

  <\remark>
    Se <math|<with|font-series|bold|X>=<with|font-series|bold|M>+<with|font-series|bold|A>=<with|font-series|bold|><with|font-series|bold|M><rprime|'>+<with|font-series|bold|A><rprime|'>>
    dove <math|<with|font-series|bold|M>,><math|<with|font-series|bold|M><rprime|'>><math|\<in\>
    <math|<with|font|cal|M><rsub|loc><rsup|c>>> e
    <math|<with|font-series|bold|A>,><math|<with|font-series|bold|A><rprime|'>>
    variazione finita. Allora abbiamo che
    <math|<with|font-series|bold|M>=><math|<with|font-series|bold|M><rprime|'>>
    e <math|<with|font-series|bold|A>=><math|<with|font-series|bold|A><rprime|'>>.
    Infatti abbiamo che <math|<with|font-series|bold|><with|font-series|bold|M><rprime|'>-<with|font-series|bold|M>=<with|font-series|bold|A><rprime|'>-<with|font-series|bold|A>\<in\>
    ><math|<with|font|cal|M><rsub|loc><rsup|c>> ed è un processo variazione
    finita e quindi deve esserro 0. Questo no sarebbe se i processi fossero
    continua a destra.
  </remark>

  <\proposition>
    <dueto|Variazione quadratica di due semimartingale>Se
    <math|\<Pi\>=<around*|{|0=t<rsub|0>\<less\>\<cdots\>\<less\>t<rsub|n>=t|}>>
    e <math|<with|font-series|bold|X>=<with|font-series|bold|M>+<with|font-series|bold|A>>
    e <math|<with|font-series|bold|Y>=<with|font-series|bold|N>+<with|font-series|bold|B>
    >sono semimartingale continue. Allora abbiamo che per
    <math|<around*|\||\<Pi\>|\|>\<rightarrow\>0>

    <\equation*>
      <big|sum><rsub|i=1><rsup|n><around*|(|X<rsub|t<rsup|i>>-X<rsub|t<rsup|i>-1>|)><around*|(|Y<rsub|t<rsup|i>>-Y<rsub|t<rsup|i>-1>|)>\<longrightarrow\><around*|\<langle\>|M,N|\<rangle\>><rsub|t>
      \ in probabilità.
    </equation*>
  </proposition>

  e vediamo che <math|<around*|\<langle\>|<with|font-series|bold|Y>,<with|font-series|bold|X>|\<rangle\>>=<around*|\<langle\>|<with|font-series|bold|M><rsup|>,<with|font-series|bold|N>|\<rangle\>>>.

  <\theorem>
    <dueto|Kunita watanabe>Sia <math|<math|<with|font-series|bold|M><rsup|>,<with|font-series|bold|N>\<in\>
    ><math|<with|font|cal|M><rsub|loc><rsup|c>>>. Consideriamo due process
    <math|H,K:\<Omega\>\<times\><around*|[|0,t|]>\<rightarrow\><with|font|Bbb|R>>
    che sono misurabili <math|<with|font|cal|F>\<otimes\><with|font|cal|B><around*|(|<around*|[|0,t|]>|)>>
    allora q.c. abbiamo la disegualgianza di Kunita-Watanabe:

    <\equation*>
      <around*|\||<big|int><rsub|0><rsup|t>H<rsub|s><text|<em|d<strong|>><math|<text|>>><text|><around*|\<langle\>|M,N|\<rangle\>><rsub|s>|\|><rsup|2>\<leq\><big|int><rsub|0><rsup|t>H<rsub|s><rsup|2><text|<em|d<strong|>><math|<text|>>><text|><around*|\<langle\>|M,M|\<rangle\>><rsub|s>\<cdot\><big|int><rsub|0><rsup|t>K<rsub|s><rsup|2><text|<em|d<strong|>><math|<text|>>><text|><around*|\<langle\>|N,N|\<rangle\>><rsub|s>
    </equation*>
  </theorem>

  <\proof>
    \;
  </proof>

  <\corollary>
    Abbiamo che q.c.\ 

    <\equation*>
      <big|int><rsub|0><rsup|t><around*|\||H<rsub|s>K<rsub|s>|\|>
      <around*|\||<text|<em|d<strong|>><math|<text|>>><text|><around*|\<langle\>|M,N|\<rangle\>><rsub|s>|\|>\<leq\><around*|(|<big|int><rsub|0><rsup|t>H<rsub|s><rsup|2><text|<em|d<strong|>><math|<text|>>><text|><around*|\<langle\>|M,M|\<rangle\>><rsub|s>|)><rsup|<frac|1|2>>\<cdot\><around*|(|<big|int><rsub|0><rsup|t>K<rsub|s><rsup|2><text|<em|d<strong|>><math|<text|>>><text|><around*|\<langle\>|N,N|\<rangle\>><rsub|s>|)><rsup|<frac|1|2>>
    </equation*>
  </corollary>

  e abbiamo anche

  <\equation*>
    <with|font|Bbb|E><big|int><rsub|0><rsup|t><around*|\||H<rsub|s>K<rsub|s>|\|>
    <around*|\||<text|<em|d<strong|>><math|<text|>>><text|><around*|\<langle\>|M,N|\<rangle\>><rsub|s>|\|>\<leq\><around*|(|<with|font|Bbb|E><big|int><rsub|0><rsup|t>H<rsub|s><rsup|2><text|<em|d<strong|>><math|<text|>>><text|><around*|\<langle\>|M,M|\<rangle\>><rsub|s>|)><rsup|<frac|1|2>>\<cdot\><around*|(|<with|font|Bbb|E><big|int><rsub|0><rsup|t>K<rsub|s><rsup|2><text|<em|d<strong|>><math|<text|>>><text|><around*|\<langle\>|N,N|\<rangle\>><rsub|s>|)><rsup|<frac|1|2>>
  </equation*>

  \;

  \;

  \;

  \;

  \;

  \;

  \;

  \;

  \;

  \;

  \;

  \;

  \;

  \;

  \;

  \;

  <chapter|>

  Definiamo

  <\equation*>
    I<rsub|t>=<big|int><rsub|0><rsup|t>H<rsub|s>dM<rsub|s>,<space|1em>t\<geq\>0
  </equation*>

  <\enumerate-roman>
    <item><math|<with|font-series|bold|M>> è una martingala continua limiata
    <math|L<rsup|2>>, <math|M<rsub|0>=0> cioè\ 

    <\equation*>
      sup<rsub|0\<leq\>t\<leq\>\<infty\>><with|font|Bbb|E><around*|[|<around*|\||M<rsub|t>|\|><rsup|2>|]>\<less\>\<infty\>
    </equation*>

    Lo spazio di tali <math|><math|<with|font-series|bold|M>> è indicato
    <math|\<bbb-H\>><math|<rsup|2>> e per processi
    <math|<with|font-series|bold|H>> opportni, risulta che anche
    <math|<with|font-series|bold|I>\<in\><math|\<bbb-H\><rsup|2>> .>

    <item>Se <math|<with|font-series|bold|M>><math|\<in\>
    <math|<with|font|cal|M><rsub|loc><rsup|c>>> si trova che
    <math|<with|font-series|bold|I>\<in\><math|
    <math|<with|font|cal|M><rsub|loc><rsup|c>><with|font|Bbb|>>>.

    <item>Se <math|<with|font-series|bold|X> >è una semimartingala definita
    come <math|<with|font-series|bold|X>=<with|font-series|bold|M>+<with|font-series|bold|A>>
    con <math|<with|font-series|bold|A>\<in\> FV>, allora

    <\equation*>
      <big|int><rsub|0><rsup|t>H<rsub|s>dX<rsub|s>=<big|int><rsub|0><rsup|t>H<rsub|s>dM<rsub|s>+<big|int><rsub|0><rsup|t>H<rsub|s>dA<rsub|s>
    </equation*>
  </enumerate-roman>

  Abbiamo le seguenti conseeguenze di appartenere allo spazio
  <math|\<bbb-H\><rsup|2>>:

  <\enumerate-roman>
    <item><with|font-series|bold|<math|M>> è UI.

    <item>Doob

    <item><math|M<rsub|t>\<rightarrow\>M<rsub|\<infty\>>>
  </enumerate-roman>

  Per<math| <math|><math|<with|font-series|bold|M>,<with|font-series|bold|N>>
  \<in\> <math|\<bbb-H\><rsup|2>>> e definiscio
  <math|<around*|(|<with|font-series|bold|M>,<with|font-series|bold|N>|)><rsub|\<bbb-H\><rsup|2>>=<with|font|Bbb|E><around*|[|<with|font-series|bold|M><rsub|\<infty\>>,<with|font-series|bold|N><rsub|\<infty\>>|]>><math|>.

  <\proposition>
    <math| <math|\<bbb-H\><rsup|2>>> è uno spazio di Hilbert.
  </proposition>

  <\proof>
    \;
  </proof>

  Ora, vogliamo definire per <math|M\<in\> ><math| <math|\<bbb-H\><rsup|2>>>
  ,

  <\equation*>
    I<rsub|t >=<big|int><rsub|0><rsup|t>H<rsub|s>dM<rsub|s>.
  </equation*>

  E usuremo la notazione <math|<with|font-series|bold|I>=<with|font-series|bold|H>\<cdot\><with|font-series|bold|M>>.
  Introduciamo lo spazio <math|L<around*|(|<with|font-series|bold|M>|)><rsup|2>>
  dei processi\ 

  <\equation*>
    H:\<Omega\>\<times\><with|font|Bbb|R><rsub|+>\<rightarrow\><with|font|Bbb|R>
  </equation*>

  progressivi e tali che

  <\equation*>
    <around*|\<\|\|\>|<with|font-series|bold|H>|\<\|\|\>><rsub|L<around*|(|<with|font-series|bold|M>|)><rsup|2>><rsup|2>=<with|font|Bbb|E><big|int><rsub|0><rsup|\<infty\>><around*|\||H<rsub|s>|\|><rsup|2><text|d<em|>><around*|\<langle\>|M,M|\<rangle\>><rsub|s>\<less\>\<infty\>
  </equation*>

  <\remark>
    <math|<with|font-series|bold|H>> è progressivo se e solo se è
    <math|\<cal-P\>>-misurabile, dove <math|\<cal-P\>> è la
    <math|\<sigma\>-algebra> progressiva su
    <math|\<Omega\>\<times\><with|font|Bbb|R><rsub|+>>.\ 

    <\equation*>
      L<around*|(|<with|font-series|bold|M>|)><rsup|2>=L<rsup|2><around*|(|\<Omega\>\<times\><with|font|Bbb|R><rsub|+>,\<cal-P\>,\<nu\><around*|(|d\<omega\>,ds|)><with|font-series|bold|>|)><rsup|>
    </equation*>
  </remark>

  dove\ 

  <\equation*>
    \<nu\><around*|(|A|)>=<with|font|Bbb|E><big|int><rsub|0><rsup|\<infty\>><with|font-series|bold|1><rsub|A><around*|(|w,s|)><text|d<em|>><around*|\<langle\>|M,M|\<rangle\>><rsub|s><around*|(|\<omega\>|)>,<space|1em>A\<in\>\<cal-P\>.
  </equation*>

  <\remark>
    <math|\<nu\>> non è una misura prodotto. Indico
    <math|\<mu\><around*|(|\<omega\>,ds|)>> la misura su
    <math|<with|font|Bbb|>><math|<with|font|Bbb|R><rsub|+>> associata a
    <math|<around*|\<langle\>|<with|font-series|bold|M>,<with|font-series|bold|M>|\<rangle\>><around*|(|\<omega\>|)><rsub|>>
    dove <math|\<mu\>> è un nucleo (kernel), cioè\ 

    <\equation*>
      \<omega\> \<mapsto\>\<mu\><around*|(|\<omega\>,B|)>,<space|1em>B\<in\>
      <with|font|cal|B><around*|(|<with|font|Bbb|R><rsub|+>|)>
    </equation*>

    è <math|<with|font|cal|F><rsub|>-misurabile > su <math|\<Omega\>>. Allora\ 

    <\equation*>
      \<nu\><around*|(|<text|d<em|>>\<omega\>,ds|)>=\<mu\><around*|(|<text|d<em|>>\<omega\>,ds|)><with|font|Bbb|P><around*|(|<text|d<em|>>\<omega\>|)>
    </equation*>
  </remark>

  Definiamo <math|<math|<with|font-series|bold|><with|font-series|bold|H>\<cdot\><with|font-series|bold|M>><math|\<in\><math|\<bbb-H\><rsup|2>>>
  > con <math|<with|font-series|bold|><math|<with|font-series|bold|M>><math|\<in\><math|\<bbb-H\><rsup|2>>>>
  e <math|<with|font-series|bold|L>\<in\>
  <math|L<around*|(|<with|font-series|bold|M>|)><rsup|2>>>.

  Fissiamo ora <math|<math|<with|font-series|bold|><with|font-series|bold|><with|font-series|bold|M>><math|\<in\><math|\<bbb-H\><rsup|2>>>>.
  Definiamo lo spazio dei <em|processi elementari>
  <with|font|cal|E>\<subset\><math|L<around*|(|<with|font-series|bold|M>|)><rsup|2>>
  che sono della forma\ 

  <\equation*>
    H<rsub|s><around*|(|\<omega\>|)>=<big|sum><rsup|p-1><rsub|k=0><with|font-series|bold|1><rsub|<around*|(|t<rsub|i>,t<rsub|i+1>|]>><around*|(|s|)>H<rsub|<around*|(|i|)>><around*|(|\<omega\>|)>
  </equation*>

  <math|0=t<rsub|0>\<less\>t<rsub|1>\<less\>\<cdots\>\<less\>t<rsub|p>=t>,
  <math|H<rsub|<around*|(|i|)>>> sono limitate e
  <math|<with|font|cal|F><rsub|t<rsub|i>>-misurabile.>\ 

  Definiamo, per <math|<with|font-series|bold|H>\<in\> ><with|font|cal|E>,

  <\eqnarray*>
    <tformat|<table|<row|<cell|<around*|(|<with|font-series|bold|H>\<cdot\><with|font-series|bold|M>|)><rsub|t>>|<cell|=>|<cell|<big|sum><rsup|p-1><rsub|k=0>H<rsub|<around*|(|i|)>><around*|(|M<rsub|t\<wedge\>t<rsub|i+1>>-M<rsub|t\<wedge\>t<rsub|i>>|)>>>|<row|<cell|>|<cell|=>|<cell|<big|sum><rsup|t<rsub|j>><rsub|i=0>H<rsub|<around*|(|i|)>><around*|(|M<rsub|t<rsub|i+1>>-M<rsub|t<rsub|i>>|)>+H<rsub|<around*|(|j|)>><around*|(|M<rsub|t<rsub|>>-M<rsub|t<rsub|j><rsub|>>|)>.>>>>
  </eqnarray*>

  <\proposition>
    <dueto|Densità di <with|font|cal|E>>Lo spazio <with|font|cal|E> è denso
    in <math|<with|font-series|bold|L>\<in\>
    <math|L<around*|(|<with|font-series|bold|M>|)><rsup|2>>>.
  </proposition>

  <\proof>
    \;
  </proof>

  <\theorem>
    La funzione <math|<with|font-series|bold|H>:\<mapsto\><with|font-series|bold|H>\<cdot\><with|font-series|bold|M>>
    definita da <with|font|cal|E> in <math|<math|<with|font-series|bold|>><math|<math|\<bbb-H\><rsup|2>>>>,
    si estende in modo univoco a una funzione\ 

    <\equation*>
      <math|<with|font-series|bold|H>\<rightarrow\>
      <with|font-series|bold|H>\<cdot\><with|font-series|bold|M>>,<space|1em>
      L<around*|(|<with|font-series|bold|M>|)><rsup|2>\<rightarrow\><math|<with|font-series|bold|>><math|<math|\<bbb-H\><rsup|2>>>
    </equation*>

    che è una isometria.

    Inolte, <math|<with|font-series|bold|H>\<cdot\><with|font-series|bold|M>>
    è l'unico elemento di <math|<math|<math|\<bbb-H\><rsup|2>>>> tale che\ 

    <\equation>
      <around*|\<langle\>|<with|font-series|bold|H>\<cdot\><with|font-series|bold|M><rsup|>,<with|font-series|bold|N>|\<rangle\>>=<with|font-series|bold|H>\<cdot\><around*|\<langle\>|<with|font-series|bold|M><rsup|>,<with|font-series|bold|N>|\<rangle\>>,<space|1em><with|font-series|bold|N>\<in\><math|<with|font-series|bold|>><math|<math|\<bbb-H\><rsup|2>>>
      </equation>

    dove <math|<around*|(|H\<cdot\><around*|\<langle\>|M,N|\<rangle\>>|)><rsub|t>>
    = <math|<big|int><rsub|0><rsup|t>H<rsub|s
    >><em|d><math|<around*|\<langle\>|M,N|\<rangle\>><rsub|s>>.
  </theorem>

  <\proof>
    \;
  </proof>

  <math|(H \<cdot\>M)<rsub|t>> si scrive anche
  <math|<big|int><rsub|0><rsup|t>H<rsub|s>dM<rsub|s>.> Abbiamo anche

  <\equation>
    <around*|\<langle\>|<with|font-series|bold|H>\<cdot\><with|font-series|bold|M><rsup|>,<with|font-series|bold|N>|\<rangle\>>=<with|font-series|bold|H>\<cdot\><around*|\<langle\>|<with|font-series|bold|M><rsup|>,<with|font-series|bold|N>|\<rangle\>>
    <label|oo>
  </equation>

  <math|si riscrive \ >

  <\equation*>
    <around*|\<langle\>|<big|int><rsub|0><rsup|.>H<rsub|s>dM<rsub|s>,N|\<rangle\>><rsub|t>=<big|int><rsub|0><rsup|t>H<rsub|s><text|d<em|>><around*|\<langle\>|M<rsup|>,N|\<rangle\>><rsub|s>
  </equation*>

  Ad esempio, segue che se <math|K,H\<in\>
  ><math|L<around*|(|<with|font-series|bold|M>|)><rsup|2>>,

  <\equation*>
    <around*|\<langle\>|<big|int><rsub|0><rsup|.>H<rsub|s>dM<rsub|s>,<big|int><rsub|0><rsup|.>K<rsub|s>dM<rsub|s>,|\<rangle\>>=<big|int><rsub|0><rsup|t>H<rsub|s><text|d<em|>><around*|\<langle\>|M<rsup|>,<big|int><rsub|0><rsup|.>K<rsub|u>dM<rsub|u>|\<rangle\>><rsub|s>=<big|int><rsub|0><rsup|t>H<rsub|s
    >K<rsub|s><text|d<em|>><around*|\<langle\>|M<rsup|>,N|\<rangle\>><rsub|s>
  </equation*>

  <\remark>
    Abbiamo che <math|<with|font-series|bold|H>\<cdot\><with|font-series|bold|M>
    > è l'unico elemento di <math|\<bbb-H\><rsup|2>> per cui vale
    <reference|oo>. Se <reference|oo> vale per
    <math|<with|font-series|bold|X>\<in\> <math|\<bbb-H\><rsup|2>,cioè >>

    <\equation*>
      <around*|\<langle\>|<with|font-series|bold|X><rsup|>,<with|font-series|bold|N>|\<rangle\>>=<with|font-series|bold|H>\<cdot\><around*|\<langle\>|<with|font-series|bold|M><rsup|>,<with|font-series|bold|N>|\<rangle\>>
      </equation*>
  </remark>

  allora ho che <math|<around*|\<langle\>|<with|font-series|bold|X-H>\<cdot\><with|font-series|bold|M><rsup|>,<with|font-series|bold|N>|\<rangle\>>=0>
  for all <math|<with|font-series|bold|N>\<in\> <math|\<bbb-H\><rsup|2>> > e
  scegliendo <math|<with|font-series|bold|N>=<with|font-series|bold|X>-><math|<with|font-series|bold|H>\<cdot\><with|font-series|bold|M>>
  abbiamo

  <\equation*>
    <around*|\<langle\>|<with|font-series|bold|X-H>\<cdot\><with|font-series|bold|M>-<with|font-series|bold|H><rsup|>\<cdot\><with|font-series|bold|M>|\<rangle\>>=0\<Rightarrow\><with|font-series|bold|X>=<with|font-series|bold|H>\<cdot\><with|font-series|bold|M>
  </equation*>

  <\remark>
    <with|font-series|bold|V> è un processo a variazione finita e <math|T> è
    un tempo di arresto\ 

    <\eqnarray*>
      <tformat|<table|<row|<cell|<around*|(|H\<cdot\>V|)><rsub|t><rsup|T>=<around*|(|H\<cdot\>V|)><rsub|t\<wedge\>T><rsup|>>|<cell|=>|<cell|<big|int><rsub|0><rsup|t\<wedge\>T>H<rsub|s>dV<rsub|s>>>|<row|<cell|>|<cell|=>|<cell|<big|int><rsub|0><rsup|t\<wedge\>T<around*|(|\<omega\>|)>>H<rsub|s><around*|(|\<omega\>|)>dV<rsub|s><around*|(|\<omega\>|)>>>|<row|<cell|>|<cell|=>|<cell|<big|int><rsub|0><rsup|t><with|font-series|bold|1><rsub|<around*|[|0,T<around*|(|\<omega\>|)>|]>><around*|(|s|)>H<rsub|s><around*|(|\<omega\>|)>dV<rsub|s><around*|(|\<omega\>|)>>>|<row|<cell|>|<cell|=>|<cell|<big|int><rsub|0><rsup|t>H<rsub|s><around*|(|\<omega\>|)>V<rsub|s><rsup|T><around*|(|\<omega\>|)>>>>>
    </eqnarray*>
  </remark>

  perché se la misura assocaita a <math|V<rsub|s><around*|(|\<omega\>|)>> è
  <math|\<mu\><around*|(|\<omega\>,ds|)>> allora \V\ 

  <\proposition>
    <with|font-series|bold|M><math|\<in\> <math|\<bbb-H\><rsup|2>>>,
    <with|font-series|bold|H>\<in\><math|<math|L<around*|(|<with|font-series|bold|M>|)><rsup|2>>>,
    <with|font-series|bold|K> prevedibile. Allora <math|K>
  </proposition>
</body>

<\initial>
  <\collection>
    <associate|font-base-size|11>
    <associate|page-medium|paper>
    <associate|page-screen-margin|false>
  </collection>
</initial>

<\references>
  <\collection>
    <associate|auto-1|<tuple|1|5|../../../../../.TeXmacs/texts/scratch/no_name_2.tm>>
    <associate|auto-2|<tuple|1|5|../../../../../.TeXmacs/texts/scratch/no_name_2.tm>>
    <associate|auto-3|<tuple|2|5|../../../../../.TeXmacs/texts/scratch/no_name_2.tm>>
    <associate|auto-4|<tuple|3|7|../../../../../.TeXmacs/texts/scratch/no_name_2.tm>>
    <associate|auto-5|<tuple|4|9|../../../../../.TeXmacs/texts/scratch/no_name_2.tm>>
    <associate|auto-6|<tuple|2|13|../../../../../.TeXmacs/texts/scratch/no_name_2.tm>>
    <associate|oo|<tuple|2.2|?|../../../../../.TeXmacs/texts/scratch/no_name_2.tm>>
  </collection>
</references>

<\auxiliary>
  <\collection>
    <\associate|toc>
      <vspace*|1fn><with|font-series|<quote|bold>|math-font-series|<quote|bold>|font-shape|<quote|small-caps>|1.<space|2spc>>
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <pageref|auto-1><vspace|0.5fn>

      <with|par-left|<quote|1tab>|1.<space|2spc>Funzioni a variazione finita.
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-2>>

      <with|par-left|<quote|1tab>|2.<space|2spc>Processi a variazione finita.
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-3>>

      <with|par-left|<quote|1tab>|3.<space|2spc>Martingale locali continue.
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-4>>

      <with|par-left|<quote|1tab>|4.<space|2spc>Variazione quadratica delle
      martingali locali continue. <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-5>>

      <vspace*|1fn><with|font-series|<quote|bold>|math-font-series|<quote|bold>|font-shape|<quote|small-caps>|2.<space|2spc>>
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <pageref|auto-6><vspace|0.5fn>
    </associate>
  </collection>
</auxiliary>