package enzet.moire.core;

import enzet.moire.util.Options;

import java.util.Map;

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
		Parser parser = new Parser(text);

		words = parser.parse();
	}

	/**
	 * Conversion to specified format. Includes parsing
     *
     * @param format resulted format
	 */
	public String convert(Format format)
	{
		parse();
		words.add(0, new Word("begin", WordType.TAG));
		words.add(new Word("end", WordType.TAG));

		if (Options.printStructure)
		{
            words.print();
		}
        return words.convert(format);
	}

	/**
	 * Conversion to specified format as book of documents.
	 */
	public Map<String, String> convertToBook(Format format, int level)
	{
		parse();

		return words.convertToBook(format, level);
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
