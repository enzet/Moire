package enzet.moire.core;

/**
 * Document
 * 
 * @author Sergey Vartanov (me@enzet.ru)
 */
public class Document
{
	String text;

	public Document(String text)
	{
		this.text = text;
	}

	public String convert(Format format)
	{
		Lexer lexer = new Lexer(text);

		String result = lexer.convert(format);

		return result;
	}
}
