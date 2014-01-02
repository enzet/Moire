package enzet.moire.core;

import java.util.List;

import enzet.moire.util.Options;

/**
 * Document
 *
 * @author Sergey Vartanov (me@enzet.ru)
 */
public class Document
{
	String text;
	Words words;

	public Document(String text)
	{
		this.text = text;
	}

	/**
	 * Parsing
	 */
	public void parse()
	{
		Lexer lexer = new Lexer(text);

		words = lexer.parse();
	}

	/**
	 * Conversion to specified format. Includes parsing
     *
     * @param format resulted format
	 */
	public String convert(Format format)
	{
		parse();

		if (Options.printStructure)
		{
            words.print();
		}
        return words.convert(format);
	}

	/**
	 * Print graphic representation of words
	 */
	public void print()
	{
		for (Word w : words)
		{
			w.print(0);
		}
	}
}
