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

	@Option(name = "-g", aliases = "--generate", usage = "Generate inner class")
	public static boolean isGenerate = false;

	// Debug printing options

	@Option(name = "--print-structure", usage = "Generate inner class")
	public static boolean printStructure = false;

	public static String innerClassFileName = "src/enzet/moire/Inner.java";
}
