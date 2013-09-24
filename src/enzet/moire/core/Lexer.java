package enzet.moire.core;

import java.util.ArrayList;
import java.util.List;

public class Lexer
{
	List<Word> words;

	/**
	 * @see #parse(char[], int)
	 */
	public Lexer(String text)
	{
		System.out.print("Parsing " + text.length() + " bytes... ");
		
		words = parse(text.toCharArray(), 0);
		
		System.out.println("done.");
	}

	int i;

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
				if (!isLetter(s[i + 1]))
				{
					ws.add(new Word(s[i + 1] + "", WordType.TAG));
					i++;
				}
				else
				{
					i++;
					String tagName = "";

					while (isLetter(s[i]))
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

	private boolean isLetter(char c)
	{
		return (c >= 'a' && c <= 'z') || (c >= '0' && c <= '9') || c == '[' || c == ']';
	}

	public boolean hasWords()
	{
		return words.size() > 0;
	}

	public Word getWord()
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

	public String convert()
	{
		String result = "";

		for (Word w : words)
		{
			result += w.convert();
		}
		return result;
	}
}
