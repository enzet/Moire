package enzet.moire.core;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.kohsuke.args4j.CmdLineParser;

import enzet.moire.core.Scheme.Section;
import enzet.moire.util.Options;
import enzet.moire.util.Util;

/**
 * Moire reader
 *
 * @author Sergey Vartanov (me@enzet.ru)
 * @version 1.0
 * @since 26-04-2012
 */
public class Reader
{
	public static String PROGRAM_NAME = "Moire";

	public static void main(String[] args) throws IOException
	{
		System.out.println(PROGRAM_NAME + ".");

		try
		{
			CmdLineParser parser = new CmdLineParser(new Options());
			parser.parseArgument(args);
		}
		catch (Exception e)
		{
			System.out.println("Error: unknown options.");
			return;
		}
		Scheme scheme = new Scheme(new BufferedReader(new FileReader(Options.schemeFileName)));

		if (!Options.isGenerate)
		{
			read(scheme);
		}
		else
		{
			generateInner(scheme);
		}
	}

	public static void read(Scheme scheme)
	{
		Format format = new Format(Options.to.toLowerCase());
		format.readFormat(scheme);

		String input = Util.get(Options.input);

		if (Options.isComments)
		{
			input = new CommentPreprocessor().preprocess(input);
		}
		input = new LanguagePreprocessor().preprocess(input, Options.language, Options.to);

		Document document = new Document(input);

		String formatted = document.convert(format);

		System.out.println(String.format("Document converted from Moire markup (%d bytes) to %s (%d bytes): %s.", input.length(), Options.to, formatted.length(), Options.output));
		Util.write(Options.output, formatted);
	}

	/**
	 * Generate source code for <code>enzet.moire.Inner</code> class. It
	 * contains methods with Java code inserted into scheme.
	 *
	 * @param scheme scheme file with input information
	 */
	public static void generateInner(Scheme scheme) throws IOException
	{
		Section formatsSection = scheme.getRoot().getChild("formats");

		StringBuilder innerClass = new StringBuilder();

		List<Format> formats = new ArrayList<Format>();

		for (Section formatSection : formatsSection.getChildren())
		{
			Format format = new Format(formatSection.getName());
			format.readFormat(scheme);

			formats.add(format);
		}
		innerClass.append("package enzet.moire;\n\n");

		for (Format format : formats)
		{
			if (format.header != null)
			{
				innerClass.append(format.header).append("\n");
			}
		}
		innerClass.append("public class Inner\n{\n");
		innerClass.append(Util.get("part"));

		for (Format format : formats)
		{
			innerClass.append(format.generateClass());
		}
		innerClass.append("}\n");

		Util.write(Options.innerClassFileName, innerClass.toString());
	}
}
