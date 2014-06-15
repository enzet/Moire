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
	public static void write(String fileName, String text) throws IOException
	{
		FileWriter writer;

		writer = new FileWriter(new File(fileName));

		writer.write(text);
		writer.close();
	}

	public static String get(String fileName) throws IOException
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

	public static boolean isLetter(char character)
	{
		return (character >= 'a' && character <= 'z') ||
			(character >= 'A' && character <= 'Z');
	}
}
