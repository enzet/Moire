package enzet.moire.core;

import java.util.ArrayList;

import enzet.moire.core.Scheme.Section.Relation;

/**
 * Word
 *
 * @author Sergey Vartanov (me@enzet.ru)
 */
public class Word
{
	public WordType type;
	public String value;
	public java.util.List<Word> children;

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

	public String getParameter(int i, Format format, boolean isClear)
	{
		Word branch = children.get(i);

		if (branch.type != WordType.BRANCH)
		{
			System.err.println("Warning: is no branch");
			return "?";
		}
		else
		{
			String s = "";

			for (Word w : branch.children)
			{
				s += (isClear ? w.screen(format) : w.convert(format));
			}
			return s;
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
			s = "	" + s;
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

	/**
	 * Word to text translation.
	 *
	 * Convert word with all subwords into the text representation.
	 */
	public String convert(Format format)
	{
		if (type == WordType.SIMPLE_WORD)
		{
			String converted = value;

			for (Relation symbol : format.getScreen())
			{
				converted = converted.replaceAll(symbol.from, symbol.to);
			}
			for (Relation symbol : format.getSymbols())
			{
				converted = converted.replaceAll(symbol.from, symbol.to);
			}
			return converted;
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
				builder.append(w.convert(format));
			}
			return builder.toString();
		}
		else if (type == WordType.TAG)
		{
			if (value.length() == 1 && !Lexer.isTagLetter(value.charAt(0)))
			{
				return value;
			}
			Rule rule = format.getRule(value, children.size());

			if (rule == null) return value;
			return rule.convert(this, format);
		}
		return value;
	}

	/**
	 * Do nothing but screen all symbols if type is simple word
	 */
	public String screen(Format format)
	{
		if (type == WordType.SIMPLE_WORD)
		{
			String converted = value;

			for (Relation symbol : format.getScreen())
			{
				converted = converted.replaceAll(symbol.from, symbol.to);
			}
			return converted;
		}
		return null;
	}
}
