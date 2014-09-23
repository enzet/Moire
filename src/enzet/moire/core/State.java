package enzet.moire.core;

import enzet.moire.util.Options;

import java.util.List;

/**
 * Parsing state of word.
 *
 * @author Sergey Vartanov (me@enzet.ru)
 */
public class State
{
	private List<Word> children;
	private List<String> level;
	public String title = "";
	public List<String> language;

	public State()
	{
		language = Options.language;
	}

	/* Getters and setters. */

	public List<Word> getChildren()
	{
		return children;
	}

	public void setChildren(List<Word> children)
	{
		this.children = children;
	}

	public List<String> getLevel()
	{
		return level;
	}

	public String getStringLevel()
	{
		StringBuilder returned = new StringBuilder();
		returned.append("../");

		if (level != null)
		{
			for (String name : level)
			{
				returned.append("../");
			}
		}
		return returned.toString();
	}

	public void setLevel(List<String> level)
	{
		this.level = level;
	}

	public String getLanguage()
	{
		return "ru";
	}
}
