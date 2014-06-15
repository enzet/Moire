package enzet.moire.core;

/**
 * Moire markup parser
 *
 * @author Sergey Vartanov (me@enzet.ru)
 */
public class Parser
{
	int i;
	char[] text;

	public Parser(String text)
	{
		this.text = text.toCharArray();
	}

	/**
	 * @see #parse(char[], int)
	 */
	public Words parse()
	{
		System.out.print("Parsing " + text.length + " bytes... ");

		Words words = parse(text, 0);
		words.add(0, new Word("begin", WordType.TAG));
		words.add(new Word("end", WordType.TAG));

		System.out.println("done.");

		return words;
	}

    /**
     * @see #parse(char[], int)
     */
    public Words parseInner()
    {
        return parse(text, 0);
    }

	/**
	 * Parse text into list of words
	 *
	 * @see Word
	 */
	public Words parse(char[] s, int beginIndex)
	{
		// Don't put debug printing here. It's very frequent method.

		Words ws = new Words();

		int length = s.length;
		StringBuffer simple = new StringBuffer("");
		Word currentParent = null;
        boolean isIgnoreSyntax = false;

		for (i = beginIndex; i < length; i++)
		{
			char c = s[i];

			if (c == '\\')
			{
				if (!simple.toString().equals("") &&
						!simple.toString().equals("\0"))
				{
					ws.add(new Word(simple.toString(), WordType.SIMPLE_WORD));
					simple = new StringBuffer("");
				}
				if (!isTagLetter(s[i + 1]))
				{
					ws.add(new Word(Character.toString(s[i + 1]),
							WordType.TAG));
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
                    for (String ign : LanguagePreprocessor.IGNORE_BEGIN)
                    {
                        if (tagName.equals(ign.substring(1)))
                        {
                            isIgnoreSyntax = true;
                            break;
                        }
                        isIgnoreSyntax = false;
                    }
					ws.add(tag);
					currentParent = tag;
				}
			}
			else if (c == '{')
			{
				if (!simple.toString().trim().equals(""))
				{
					ws.add(new Word(simple.toString(), WordType.SIMPLE_WORD));
				}
				simple = new StringBuffer("");

				Word branch = new Word("", WordType.BRANCH);

                if (isIgnoreSyntax)
                {
                    i++;
                    while (!(s[i] == '}' && s[i - 1] != '\\'))
                    {
                        simple.append(s[i]);
                        i++;
                    }
                    branch.addChild(new Word(simple.toString(),
		                    WordType.SIMPLE_WORD));
                    simple = new StringBuffer("");
                }
                else
                {
				    branch.addChildren(parse(s, i + 1));
                }
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
