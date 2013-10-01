package enzet.moire.core;

import enzet.moire.core.Scheme.Section;
import enzet.moire.core.Scheme.Section.Relation;
import java.util.ArrayList;
import java.util.List;

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
            
            Section tagsSection = currentFormat.getChild("tags");
            List<Relation> relations = tagsSection.getRelations();
            
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
            Section symbolsSection = currentFormat.getChild("symbols");
            symbols = symbolsSection.getRelations();
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
    
    public List<Relation> getSymbols()
    {
        return symbols;
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
}
