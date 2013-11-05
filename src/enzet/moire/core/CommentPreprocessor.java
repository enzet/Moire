package enzet.moire.core;

import java.util.Arrays;

/**
 * Comment preprocessor
 *
 * @author Sergey Vartanov (me@enzet.ru)
 */
public class CommentPreprocessor
{
	private static char FIRST = '/';
	private static char SECOND = '*';
	private static char SCREEN = '\\';

	public String preprocess(String text)
	{
		System.out.print("Comment preprocessing...");

		char[] array = new char[text.length()];
		int k = 0;

		for (int i = 0; i < text.length(); i++)
		{
			char pc = i == 0 ? ' ' : text.charAt(i - 1);
			char c1 = text.charAt(i);
			char c2 = i == text.length() - 1 ? ' ' : text.charAt(i);

			if (pc != SCREEN && c1 == FIRST && c2 == SECOND)
			{
				while (!(text.charAt(i) == SECOND && text.charAt(i + 1) == FIRST))
				{
					i++;
				}
				i += 2;
				c1 = text.charAt(i);
			}
			if (k < text.length())
			{
				array[k++] = c1;
			}
		}
		System.out.println(" done.");

		return new String(Arrays.copyOf(array, k));
	}
}
