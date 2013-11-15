*Moiré* is a simple multipurpose markup.

Writing on *Moiré*
-------------------

Syntax definition of *Moiré* is [here](http://enzet.ru/en/program/moire).

Conversion *Moiré* code into other formats
-------------------------------------------

Requirements: Java.

    java -jar Moire.jar -i <Moiré input file> -t <output format> -o <output file> <other options>
    

### Options ###

``-i`` or ``--input``—input file in *Moiré* format;

``-o`` or ``--output``—output file;

``-t`` or ``--to``—format of output file. May be ``html``, ``text`` or ``markdown``;

``-s`` or ``--scheme``—scheme file name.

Writing scheme files for conversion into new formats
----------------------------------------------------

Requirements: ``javac``, Apache Ant.
