package enzet.moire.util;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

/**
 * Utility functions
 *
 * @author Sergey Vartanov (me@enzet.ru)
 */
public class Util
{
	public static void write(String fileName, String text)
	{
		FileWriter writer;
		try
		{
			writer = new FileWriter(new File(fileName));

			writer.write(text);
			writer.close();
		}
		catch (IOException e)
		{
			System.out.println("Error: cannot write to " + fileName + ".");
		}
	}

	public static String get(String fileName)
	{
		try
		{
			BufferedReader reader = new BufferedReader(new FileReader(fileName));

			String line;
			StringBuilder content = new StringBuilder();

			while ((line = reader.readLine()) != null)
			{
				content.append(line).append("\n");
			}
			reader.close();

			return content.toString();
		}
		catch (Exception e)
		{
			System.out.println("Error: cannot read from " + fileName + ".");
		}
		return null;
	}

	public static boolean isLetter(char character)
	{
		return (character >= 'a' && character <= 'z') ||
			(character >= 'A' && character <= 'Z');
	}
}
