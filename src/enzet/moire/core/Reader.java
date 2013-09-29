package enzet.moire.core;

import enzet.moire.core.Scheme.Section;
import java.io.IOException;

import org.kohsuke.args4j.CmdLineParser;

import enzet.moire.util.Options;
import enzet.moire.util.Util;
import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

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

    public static List<Rule> rules;
        
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
        Scheme scheme = new Scheme(new BufferedReader(new FileReader("scheme")));
        
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
}
