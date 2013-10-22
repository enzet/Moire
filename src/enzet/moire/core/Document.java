package enzet.moire.core;

import java.util.List;

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

		String result = "";

		for (Word w : words)
		{
			result += w.convert(format);
		}
		return result;
	}

	/**
	 * Returns word from the main list
	 */
	public Word getWord(int number)
	{
		return words.remove(0);
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
