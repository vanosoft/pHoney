.. image:: https://github.com/vanosoft/pHoney/blob/1.9.8a/docs/cosial_logo.png?raw=true

.. image:: https://bit.ly/gitloadbutton
   :target: https://github.com/vanosoft/cHoney/archive/refs/heads/1.9.8a.zip

Honey - *универсальный язык программирования*
-----------

*АННОТАЦИЯ*

**Honey** - это язык программирования, ориентированный на  производительность, гибкость и простоту использования.
Код на нём можно скомпилировать в исполняемый либо бинарный файл, а так же перевести на другой (интерпретируемый)
язык программирования (например JS, для создания web-приложения).

*ОПИСАНИЕ*

В современном мире очень распространены интерпретируемые языки программирования, которые медленные в отличие от компилируемых.
Однако, производительность пожертвована ради простоты использования и возможности запускать код в "сыром" виде. также,
существуют интерпретируемо-компилируемые языки программирования, но они не отличаются от интерпретируемых по 
cкорости, а от компилируемых по сложности использования.

Цель моего проекта - сделать свой простой язык программирования (далее ЯП), который можно как интерпретировать,
так и компилировать, но ещё и переводить на другие языки. Это бывает очень полезно, ведь можно написать программу
на моем языке, и скомпилировать её для, например, MS Windows, и перевести на JS, собрав тем самым web-приложение.

Для создания своего ЯП я использовую язык Python.
Принцип работы состоит в том, что код, написаный на Honey делится на синтаксические единицы, которые потом
обрабатываются с помощью Оптимизатора, который удаляет неиспользуемые переменные и упрощает выражения по мере
возмости. Далее, в зависимости от того, чего требует программист, парсер либо переводит всё это на С и компилирует,
либо переводит на интерпретируемый язык программирования, либо исполняет (т.е. интерпретирует).

Я закончил начальную стадию проекта, то есть написал лексер.

*СТРУКТУРА ПРОЕКТА*

файловая структура архива с проектом выглядит так:

git: pHoney 1.9.8 alpha

  - example
  
    - test.hny
    
  - bin
  
    - honey.exe
    
    - hiimgr.exe
    
  - src
  
    - honey.py
    
    - modules...
    
  - readme.md
  
  - readme.htm

-----------
-----------

Honey - *universal programming language*
-----------


*ABSTRACT*

**Honey** is a programming language focused on performance, flexibility and ease of use.
The code on it can be compiled into an executable or binary file, as well as translated into another (interpreted)
programming language (for example, JS, to create a web application).

*DESCRIPTION*

Interpreted programming languages are very common in the modern world, which are slow in contrast to compiled ones.
However, performance is sacrificed for the sake of ease of use and the ability to run the code in its "raw" form. also,
there are interpreted-compiled programming languages, but they do not differ from interpreted ones in terms of
speed, but from compiled ones in terms of complexity of use.

The goal of my project is to make my own simple programming language (hereinafter referred to as pHoney), which can be both interpreted
and compiled, but also translated into other languages. This can be very useful, because you can write a program
in my language, and compile it for, for example, MS Windows, and translate it into JS, thereby assembling a web application.

To create my own programming language, I use the Python language.
The principle of operation is that the code written in pHoney is divided into syntactic units, which are then
processed using an Optimizer that removes unused variables and simplifies expressions as
needed. Further, depending on what the programmer requires, the parser either translates all this into C and compiles,
or translates it into an interpreted programming language, or executes (i.e. interprets).

I finished the initial stage of the project, that is, I wrote a lexer.

*PROJECT STRUCTURE*

the file structure of the archive with the project looks like this:

git: pHoney 1.9.8 alpha

  - example
  
    - test.hny
    
  - bin
  
    - honey.exe
    
    - hiimgr.exe
    
  - src
  
    - honey.py
    
    - modules...
    
  - readme.md
  
  - readme.htm
