package enzet.moire.core;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import enzet.moire.core.Scheme.Section;
import enzet.moire.core.Scheme.Section.Relation;

/**
 * Format.
 * <br />
 * E.g. HTML, TeX, Markdown.
 *
 * @author Sergey Vartanov (me@enzet.ru)
 */
public class Format
{
	private String name;

	private String caption;
	private String extension;

	/**
	 * Super format.
	 */
	Format parent;

	List<Rule> rules;
	List<Relation> symbols;
	List<Relation> screen;
	String header;
	String initialActions;

	public Format(String name)
	{
		this.name = name;
		rules = new ArrayList<Rule>();
	}

	/**
	 * Reading current format from scheme.
	 *
	 * @param scheme Moire scheme
	 * @param formats currently parsed formats (it means extended format should
	 *                be defined before format extending it)
	 */
	public void readFormat(Scheme scheme, Map<String, Format> formats)
	{
		try
		{
			Section currentFormat =
					scheme.getRoot().getChild("formats").getChild(name);

			if (currentFormat == null)
			{
				System.err.println("Error: no such format in scheme: " + name);
			}
			List<Relation> formatParameters = currentFormat.getRelations();

			if (formatParameters != null)
			{
				for (Relation r : formatParameters)
				{
					if (r.from.equals("name"))
					{
						caption = r.to;
					}
					if (r.from.equals("extension"))
					{
						extension = r.to;
					}
					/* Parent format reading. */

					if (r.from.equals("extends"))
					{
						parent = formats.get(r.to);

						if (parent == null)
						{
							System.err.println("Error: has no parent format " +
									r.to + " for format " + name);
							return;
						}
					}
				}
			}
			/* Rules reading. */

			Section tags = currentFormat.getChild("tags");

			if (tags == null)
			{
				System.err.println("Error: format " + name + " has no tags.");
				return;
			}
			List<Relation> relations = tags.getRelations();

			for (Relation r : relations)
			{
				try
				{
					rules.add(new Rule(r.from, r.to));
				}
				catch (Exception e)
				{
					System.err.println("Error: irregular rule for " + r + ".");
					e.printStackTrace();
				}
			}
			Section symbolsSection = currentFormat.getChild("symbols");
			if (symbolsSection != null)
			{
				symbols = symbolsSection.getRelations();
			}
			Section screenSection = currentFormat.getChild("screen");
			if (screenSection != null)
			{
				screen = screenSection.getRelations();
			}
			Section headerSection = currentFormat.getChild("header");
			if (headerSection != null)
			{
				header = headerSection.getString();
			}
			Section initSection = currentFormat.getChild("init");
			if (initSection != null)
			{
				initialActions = initSection.getString();
			}
		}
		catch (Exception e)
		{
			System.err.println("Error: irregular scheme file.");
			e.printStackTrace();
		}
	}

	/**
	 * Returns own rule or parent rule.
	 */
	public Rule getRule(String name, int parameters)
	{
		for (Rule rule : rules)
		{
			if (rule.getName().equals(name) &&
					rule.getParameters() == parameters)
			{
				return rule;
			}
		}
		if (parent == null)
		{
			return null;
		}
		return parent.getRule(name, parameters);
	}

	public String generateClass()
	{
		StringBuilder clazz = new StringBuilder();

		clazz.append("\tpublic static class ").append(name.toUpperCase())
				.append("\n\t{\n");

		if (initialActions != null)
		{
			clazz.append(initialActions).append("\n");
		}

		for (Rule r : rules)
		{
			clazz.append(r.generateMethods());
		}
		clazz.append("\t}\n\n");

		return clazz.toString();
	}

	public void print()
	{
		for (Rule rule : rules)
		{
			System.out.println(rule.toString());
		}
	}

	// Getters and setters

	public String getName()
	{
		return name;
	}

	public List<Relation> getSymbols()
	{
		if (symbols != null)
		{
			return symbols;
		}
		if (parent == null)
		{
			return null;
		}
		return parent.getSymbols();
	}

	public List<Relation> getScreen()
	{
		if (screen != null)
		{
			return screen;
		}
		if (parent == null)
		{
			return null;
		}
		return parent.getScreen();
	}

	public String getCaption()
	{
		if (caption != null)
		{
			return caption;
		}
		if (parent == null)
		{
			return null;
		}
		return parent.getCaption();
	}
}
