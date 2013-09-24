package enzet.moire.core;

import java.io.File;
import java.util.ArrayList;

import enzet.moire.util.Options;

public class Word
{
	public WordType type;
	public String value;
	public java.util.List<Word> children;

	// Static fields

	static boolean isRussian;

	static String[] id = {"", "", "", "", "", "", "", "", ""};

	public Word(String s, WordType wordType)
	{
		type = wordType;
		value = s;
		children = new ArrayList<Word>();
	}

	public void addChild(Word child)
	{
		children.add(child);
	}

	public void addChildren(java.util.List<Word> words)
	{
		children.addAll(words);
	}

	public Word getChild1()
	{
		try
		{
			Word w = children.remove(0);

			return w;
		}
		catch (Exception e)
		{
			//Logger.error("tag " + value + " has no more children");
			//Logger.log(id[0] + " " + id[1] + " " + id[2] + " " + id[3] + " " + id[4] + " " + id[5]);
			return new Word("NOTHING", WordType.SIMPLE_WORD);
		}
	}

	public String getb(int i)
	{
		try
		{
			Word branch = children.get(i);

			if (branch.type != WordType.BRANCH)
			{
				System.out.println("Warning: is no branch");
				return "?";
			}
			else
			{
				String s = "";

				for (Word w : branch.children)
				{
					s += w.convert();
				}
				return s;
			}
		}
		catch (Exception e)
		{
			return "?";
		}
	}

	public void print(int level)
	{
		String s = "\"" + value + "\"";

		s = s.replaceAll("\n", "").trim();
		if (s.length() > 50) s = s.substring(0, 50);

		if (type == WordType.TAG) s = "tag " + s;
		if (type == WordType.BRANCH) s = "branch " + s;

		for (int i = 0; i < level; i++)
		{
			s = "    " + s;
		}

		System.out.println(s);

		for (Word w : children)
		{
			w.print(level + 1);
		}
	}

	@Override
	public String toString()
	{
		String s = value;

		s = s.replaceAll("\n", "^").trim();
		if (s.length() > 50) s = s.substring(0, 50);

		return "<" + s + ">";
	}

	public boolean hasChild(int i)
	{
		return children.size() > i;
	}

    /**
     * Convert word with all subwords into the text representation
     */
	public String convert() 
	{
		if (type == WordType.SIMPLE_WORD)
		{
            return value; // TODO: with convertion
		}
		else if (type == WordType.FORMULA)
		{
            return "$" +  value + "$";
		}
		else if (type == WordType.BRANCH)
		{
			StringBuilder builder = new StringBuilder();

			for (Word w : children)
			{
				builder.append(w.convert());
			}
			return builder.toString();
		}
		else if (type == WordType.TAG)
		{
            Rule rule = Reader.getRule(value, children.size());
            
            if (rule == null) return value;
            return rule.convert(this);
		}
		return value;
	}
}
