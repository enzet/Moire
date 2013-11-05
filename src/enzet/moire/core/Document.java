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
	List<Word> words;

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
	 * Conversion
	 */
	public String convert(Format format)
	{
		parse();

		if (Options.printStructure)
		{
			for (Word word : words)
			{
				word.print(0);
			}
		}
		StringBuilder returned = new StringBuilder();

		for (Word w : words)
		{
			returned.append(w.convert(format));
		}
		return returned.toString();
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
