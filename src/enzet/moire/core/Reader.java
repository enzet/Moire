package enzet.moire.core;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.StringWriter;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;
import java.util.jar.JarEntry;
import java.util.jar.JarFile;

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

	static Map<String, Format> formats;

	public static void main(String[] args) throws IOException
	{
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
		Scheme scheme = createScheme();

		if (Options.printScheme)
		{
			scheme.print();
		}
		readFormats(scheme);

		if (!Options.isGenerate)
		{
			read(scheme);
		}
		else
		{
			generateInner(scheme);
		}
	}

	private static Scheme createScheme() throws IOException, FileNotFoundException
	{
		if (Options.schemeFileName != null)
		{
			File schemeFile = new File(Options.schemeFileName);

			if (!schemeFile.exists())
			{
				System.err.println("Error: scheme file \"" + Options.schemeFileName + "\" does not exist.");
				return null;
			}
			if (!schemeFile.isFile())
			{
				System.err.println("Error: scheme file \"" + Options.schemeFileName + "\" is not file.");
				return null;
			}
			if (!schemeFile.canRead())
			{
				System.err.println("Error: cannot read from scheme file \"" + Options.schemeFileName + "\".");
				return null;
			}
		}
		URL mainClassURL = Reader.class.getResource("Reader.class");
		String path = mainClassURL.getFile();

		// Running from JAR file

		if (path.indexOf(':') != -1 && path.indexOf('!') != -1)
		{
			String jarFilePath = path.substring(path.indexOf(':') + 1, path.indexOf('!'));
			JarFile jar = new JarFile(jarFilePath);
			JarEntry file = jar.getJarEntry("scheme");

			if (file != null)
			{
				InputStream is = jar.getInputStream(file);
				StringWriter writer = new StringWriter();

				while (is.available() > 0)
				{
					writer.write(is.read());
				}
				writer.close();
				is.close();
				return new Scheme(writer);
			}
			else
			{
				System.err.println("Error: scheme file is not found in JAR.");
			}
		}
		System.out.println(path);

		return new Scheme(new BufferedReader(new FileReader(Options.schemeFileName)));
	}

	public static void read(Scheme scheme)
	{
		Format format = new Format(Options.to.toLowerCase());
		format.readFormat(scheme);

		String input = Util.get(Options.input);

		if (!Options.isKeepComments)
		{
			input = new CommentPreprocessor().preprocess(input);
		}
		input = new LanguagePreprocessor().preprocess(input, Options.language, Options.to);

		Document document = new Document(input);

		String formatted = document.convert(format);

		System.out.println(String.format("Document converted from Moire markup (%d bytes) to %s (%d bytes): %s.", input.length(), Options.to, formatted.length(), Options.output));
		Util.write(Options.output, formatted);
	}

	private static void readFormats(Scheme scheme)
	{
		Section formatsSection = scheme.getRoot().getChild("formats");

		formats = new HashMap<String, Format>();

		for (Section formatSection : formatsSection.getChildren())
		{
			Format format = new Format(formatSection.getName());
			format.readFormat(scheme);

			formats.put(formatSection.getName(), format);
		}
	}

	public static Format getFormat(String formatName)
	{
		return formats.get(formatName);
	}

	/**
	 * Generate source code for <code>enzet.moire.Inner</code> class. It
	 * contains methods with Java code inserted into scheme.
	 *
	 * @param scheme scheme file with input information
	 */
	public static void generateInner(Scheme scheme) throws IOException
	{
		StringBuilder innerClass = new StringBuilder();

		innerClass.append("package enzet.moire;\n\n");
		innerClass.append("import enzet.moire.core.Reader;\n\n");
		innerClass.append("import enzet.moire.core.Word;\n\n");

		for (Format format : formats.values())
		{
			if (format.header != null)
			{
				innerClass.append(format.header).append("\n");
			}
		}
		innerClass.append("public class Inner\n{\n");
		innerClass.append(Util.get("part"));

		for (Format format : formats.values())
		{
			innerClass.append(format.generateClass());
		}
		innerClass.append("}\n");

		Util.write(Options.innerClassFileName, innerClass.toString());
	}
}
