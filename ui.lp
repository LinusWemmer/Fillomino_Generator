elem(w, window,root).

    elem(foo,container,w).
    attr(foo,width,100).
    attr(foo,heigth,100).
    elem(dd(X,Y),dropdown_menu,foo):-pos(X,Y).
        attr(dd(X,Y),width,50):-pos(X,Y).
        attr(dd(X,Y),height,50):-pos(X,Y).
        attr(dd(X,Y),grid_column,X):-pos(X,Y).
        attr(dd(X,Y),grid_row,Y):-pos(X,Y).
        attr(dd(X,Y),class,("border-dark";"bg-primary")):-pos(X,Y).
