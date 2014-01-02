package enzet.moire.core;

import java.util.ArrayList;

/**
 * Array list of words
 *
 * @author Sergey Vartanov (me@enzet.ru)
 */
public class Words extends ArrayList<Word>
{
    public String convert(Format format)
    {
        StringBuilder returned = new StringBuilder();

        for (Word w : this)
        {
            returned.append(w.convert(format));
        }
        return returned.toString();
    }

    public void print()
    {
        for (Word word : this)
        {
            word.print(0);
        }
    }
}
