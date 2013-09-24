package enzet.moire.core;

/**
 * Rule
 *
 * @author Sergey Vartanov (me@enzet.ru)
 */
public class Rule
{
    private String name;
    private int parameters;
    
    private String rule;
    
    public Rule(String key, String value)
    {
        name = key.substring(0, key.indexOf(" "));
        parameters = Integer.parseInt(key.substring(key.indexOf(" ")).trim());
        rule = value;
    }
    
    public String convert(Word word)
    {
        String returned = rule;
        
        for (int i = 0; i < parameters; i++)
        {
            returned = returned.replaceAll("\\\\" + (i + 1), getWordParameter(word, i));
        }
        return returned;
    }

    private String getWordParameter(Word word, int i)
    {
        Word branch = word.children.get(i);

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
    
    // Getters and setters
    
    public String getName()
    {
        return name;
    }

    public void setName(String name)
    {
        this.name = name;
    }

    public int getParameters()
    {
        return parameters;
    }

    public void setParameters(int parameters)
    {
        this.parameters = parameters;
    }
}
