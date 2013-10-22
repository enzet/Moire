package enzet.moire.core;

import java.util.ArrayList;
import java.util.List;

/**
 * Moire markup lexer
 *
 * @author Sergey Vartanov
 */
public class Lexer
{
	int i;
	char[] text;

	public Lexer(String text)
	{
		this.text = text.toCharArray();
	}

	/**
	 * @see #parse(char[], int)
	 */
	public List<Word> parse()
	{
		List<Word> words;

		System.out.print("Parsing " + text.length + " bytes... ");

		words = parse(text, 0);

		System.out.println("done.");

		return words;
	}

	/**
	 * Parse text into list of words
	 *
	 * @see Word
	 */
	public List<Word> parse(char[] s, int beginIndex)
	{
		// Don't put debug printing here. It's very frequent method.
		
		List<Word> ws = new ArrayList<Word>();

		int length = s.length;
		StringBuffer simple = new StringBuffer("");
		Word currentParent = null;

		for (i = beginIndex; i < length; i++)
		{
			char c = s[i];

			if (c == '\\')
			{
				if (!simple.toString().equals(""))
				{
					ws.add(new Word(simple.toString(), WordType.SIMPLE_WORD));
					simple = new StringBuffer("");
				}
				if (!isTagLetter(s[i + 1]))
				{
					ws.add(new Word(Character.toString(s[i + 1]), WordType.TAG));
					i++;
				}
				else
				{
					i++;
					String tagName = "";

					while (isTagLetter(s[i]))
					{
						tagName += s[i];
						i++;
					}
					if (s[i] != ';') i--;

					Word tag = new Word(tagName, WordType.TAG);
					ws.add(tag);
					currentParent = tag;
				}
			}
			else if (c == '{')
			{
				// Don't add white spaces before tag arguments

				if (!simple.toString().trim().equals(""))
				{
					ws.add(new Word(simple.toString(), WordType.SIMPLE_WORD));
				}
				simple = new StringBuffer("");

				Word branch = new Word("", WordType.BRANCH);
				branch.addChildren(parse(s, i + 1));

				if (currentParent != null)
				{
					currentParent.addChild(branch);
				}
				else
				{
					ws.add(branch);
				}
			}
			else if (c == '}')
			{
				if (!simple.toString().equals(""))
				{
					ws.add(new Word(simple.toString(), WordType.SIMPLE_WORD));
				}
				return ws;
			}
			else
			{
				simple.append(c);
			}
		}
		if (!simple.toString().equals(""))
		{
			ws.add(new Word(simple.toString(), WordType.SIMPLE_WORD));
		}
		return ws;
	}

	/**
	 * If tag value may contains that letter
	 * 
	 * @param c letter
	 */
	public static boolean isTagLetter(char c)
	{
		return (c >= 'a' && c <= 'z') || (c >= '0' && c <= '9');
	}
}
