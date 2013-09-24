package enzet.moire.core;

import java.util.Arrays;

/**
 * Comment preprocessor
 *
 * @author Sergey Vartanov (me@enzet.ru)
 */
public class CommentPreprocessor
{
	public String preprocess(String text)
	{
		System.out.print("Comment preprocessing...");

		char[] newText = new char[text.length()];
		int k = 0;

		for (int i = 0; i < text.length(); i++)
		{
			char c = text.charAt(i);

			if (c == '/' && text.charAt(i + 1) == '*')
			{
				while (!(text.charAt(i) == '*' && text.charAt(i + 1) == '/'))
					i++;

				i++;
				i++;
				c = text.charAt(i);
			}
			k++;

			if (k < text.length()) newText[k] = c;
		}
		newText[k] = '\0';
		
		char[] newNewText = new char[k];
		newNewText = Arrays.copyOf(newText, k);
		
		System.out.println(" done.");

		return new String(newNewText);
	}
}
