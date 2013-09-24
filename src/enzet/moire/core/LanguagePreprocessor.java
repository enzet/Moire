package enzet.moire.core;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.StringReader;
import java.util.Arrays;

/**
 * Language preprocessor
 *
 * @author Sergey Vartanov (me@enzet.ru)
 */
public class LanguagePreprocessor
{
	static String BEGIN = "[", END = "]";
	
	public String preprocess(String text, String language)
	{
		if (language == null || language.equals("")) return text;
		
		char c1 = language.charAt(0);
		char c2 = language.charAt(1);
		
		//System.out.print("Language preprocessing...");

		char[] newText = new char[text.length()];
		int k = 0;

		for (int i = 0; i < text.length(); i++)
		{
			char c = text.charAt(i);

			if (c == '[' && text.charAt(i + 1) == c1 && text.charAt(i + 2) == c2)
			{
				i++; i++; // two language characters deleting
				i++; // space deleting
				continue;
			}
			if (c == ']') continue;
			if (c == '[' && (text.charAt(i + 1) != c1 || text.charAt(i + 2) != c2))
			{
				while (text.charAt(i) != ']')
					i++;
				continue;
			}
			k++;

			if (k < text.length()) newText[k] = c;
		}
		newText[k] = '\0';
		
		char[] newNewText;
		newNewText = Arrays.copyOf(newText, k);
		
		return new String(newNewText);
	}
	
	public String preprocess_old(String content, String language) throws IOException
	{
		BufferedReader reader = new BufferedReader(new StringReader(content));

		boolean isLang = false, isOther = true;

		String line;
		StringBuilder result = new StringBuilder();

		while ((line = reader.readLine()) != null)
		{
			String line1 = line.trim();

			if (line1.equals(BEGIN + language))
			{
				isLang = true;
				isOther = false;
			}
			else if (line1.startsWith(BEGIN))
			{
				isLang = false;
				isOther = false;
			}
			else if (line1.equals(END))
			{
				isLang = false;
				isOther = true;
			}
			else
			{
				if (isOther || isLang)
				{
					result.append(line).append("\n");
					continue;
				}
			}
		}
		return result.toString();
	}
}
