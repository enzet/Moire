package enzet.moire.core;

import enzet.moire.core.Scheme.Section;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * Format
 *
 * @author Sergey Vartanov (me@enzet.ru)
 */
public class Format
{
    String name;
    
    List<Rule> rules;
    Map<String, String> symbols;
    
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
            Map<String, String> relations = tagsSection.getRelations();
            
            for (String k : relations.keySet())
            {
                try
                {
                    rules.add(new Rule(k, relations.get(k)));
                }
                catch (Exception e)
                {
                    System.err.println("irregular rule for " + k);
                }
            }
            Section symbolsSection = currentFormat.getChild("symbols");
            symbols = symbolsSection.getRelations();
        }
        catch (Exception e)
        {
            System.err.println("irregular scheme file");
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
    
    public Map<String, String> getSymbols()
    {
        return symbols;
    }
}
