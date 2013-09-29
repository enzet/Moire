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
    
    public String convert(Word word, Format format)
    {
        String returned = rule;
        
        for (int i = 0; i < parameters; i++)
        {
            returned = returned.replaceAll("\\\\" + (i + 1), word.getParameter(i, format, false));
            returned = returned.replaceAll("\\\\c" + (i + 1), word.getParameter(i, format, true));
        }
        return returned;
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
