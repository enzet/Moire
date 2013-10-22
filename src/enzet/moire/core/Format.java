package enzet.moire.core;

import java.util.ArrayList;
import java.util.List;

import enzet.moire.core.Scheme.Section;
import enzet.moire.core.Scheme.Section.Relation;

/**
 * Format
 *
 * @author Sergey Vartanov (me@enzet.ru)
 */
public class Format
{
    String name;

    List<Rule> rules;
    List<Relation> symbols;
    List<Relation> screen;

    public Format(String name)
    {
        this.name = name;
        rules = new ArrayList<Rule>();
    }

    public void readFormat(Scheme scheme)
    {
        try
        {
            Section currentFormat = scheme.getRoot().getChild("formats").getChild(name);
			List<Relation> relations = currentFormat.getChild("tags").getRelations();

            for (Relation r : relations)
            {
                try
                {
                    rules.add(new Rule(r.from, r.to));
                }
                catch (Exception e)
                {
                    System.err.println("irregular rule for " + r);
                }
            }
			symbols = currentFormat.getChild("symbols").getRelations();
			screen = currentFormat.getChild("screen").getRelations();
        }
        catch (Exception e)
        {
            System.err.println("Error: irregular scheme file.");
        }
    }

    public Rule getRule(String name, int parameters)
    {
        for (Rule rule : rules)
        {
            if (rule.getName().equals(name) && rule.getParameters() == parameters)
            {
                return rule;
            }
        }
        return null;
    }

	public String generateClass()
	{
		StringBuilder clazz = new StringBuilder();

		clazz.append("\tpublic static class " + name.toUpperCase() + "\n\t{\n");

		for (Rule r : rules)
		{
			clazz.append(r.generateMethods());
		}
		clazz.append("\t}\n\n");

		return clazz.toString();
	}

	// Getters and setters

    public List<Relation> getSymbols()
    {
        return symbols;
    }

	public List<Relation> getScreen()
	{
		return screen;
	}
}
