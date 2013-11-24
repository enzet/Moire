Moiré is a simple multipurpose markup.

Writing on Moiré
----------------

Moiré syntax definition is [here](http://enzet.ru/en/program/moire).

Conversion Moiré code into other formats
----------------------------------------

Requirements: Java, ``javac``, Apache Ant.

Build Moiré: ``ant dist`` and run it:

    java -jar Moire.jar -i <Moiré input file> -t <output format> -o <output file> <other options>
    

### Options ###

``-i`` or ``--input``—input file in *Moiré* format;

``-o`` or ``--output``—output file;

``-t`` or ``--to``—format of output file. May be ``html``, ``text`` or ``markdown``;

``-s`` or ``--scheme``—scheme file name.

