package enzet.moire.util;

import java.util.List;

import org.kohsuke.args4j.Option;

/**
 * Options
 *
 * @author Sergey Vartanov (me@enzet.ru)
 */
public class Options
{
	public static String partFileName = "part.java";
    public static String defaultSchemeFileName = "default.moirescheme";

	// Main options

	@Option(name = "-i", aliases = "--input", usage = "Input file with Moire syntax")
	public static String input;

	@Option(name = "-o", aliases = "--output", usage = "Output file")
	public static String output;

	@Option(name = "-t", aliases = "--to", usage = "Output format")
	public static String to;

	@Option(name = "-l", aliases = "--language", usage = "Language preprocessing")
	public static List<String> language;

	@Option(name = "-kc", aliases = "--keep-comments", usage = "Don't preprocess comments")
	public static boolean isKeepComments = false;

	@Option(name = "-s", aliases = "--scheme", usage = "Scheme file")
	public static String schemeFileName;

	@Option(name = "-b", aliases = "--book", usage = "Create book instead of single file with level")
	public static int bookLevel = -1;

	@Option(name = "-g", aliases = "--generate", usage = "Generate inner class")
	public static boolean isGenerate = false;

	public static String innerClassFileName = "src/enzet/moire/Inner.java";

	// Debug printing options

	@Option(name = "--print-structure", usage = "Print input file structure.")
	public static boolean printStructure = false;

	@Option(name = "--print-scheme", usage = "Print scheme file structure.")
	public static boolean printScheme = false;
}
