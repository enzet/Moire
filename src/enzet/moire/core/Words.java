package enzet.moire.core;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

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
		State state = new State();

        for (Word word : this)
        {
            returned.append(word.convert(format, state));
        }
        return returned.toString();
    }

	public Map<String, String> convertToBook(Format format, int level)
	{
		Map<String, String> pages = new HashMap<String, String>();

		State state = new State();

		List<String> fileNames = new ArrayList<String>();
		StringBuilder page = new StringBuilder();
		page.append(new Word("begin", WordType.TAG).convert(format, state));

		for (Word word : this)
		{
			if (word.type == WordType.TAG)
			{
				Integer currentLevel = null;

				try
				{
					currentLevel = Integer.parseInt(word.value);
				}
				catch (NumberFormatException e) {}

				if (currentLevel != null && currentLevel <= level &&
						word.hasParameter(1))
				{
					page.append(new Word("end", WordType.TAG)
							.convert(format, state));

					String fileName = "";

					for (String fn : fileNames)
					{
						fileName += fn + "/";
					}
					pages.put(fileName + "index.html", page.toString());

					if (fileNames.size() < currentLevel)
					{
						fileNames.add(
								word.getParameter(1, format, false, state));
					}
					else
					{
						fileNames.set(currentLevel - 1,
								word.getParameter(1, format, false, state));
					}
					while (fileNames.size() > currentLevel)
					{
						fileNames.remove(fileNames.size() - 1);
					}
					state.setLevel(fileNames);

					page = new StringBuilder()
							.append(new Word("begin", WordType.TAG)
									.convert(format, state));
				}
			}
			page.append(word.convert(format, state));
		}
		page.append(new Word("end", WordType.TAG).convert(format, state));

		String fileName = "";

		for (String fn : fileNames)
		{
			fileName += fn + "/";
		}
		pages.put(fileName + "index.html", page.toString());

		return pages;
	}

    public void print()
    {
        for (Word word : this)
        {
            word.print(0);
        }
    }
}
