package enzet.moire.test;

import enzet.moire.core.Format;
import enzet.moire.core.Parser;
import enzet.moire.core.Scheme;

import junit.framework.Assert;
import org.junit.Test;
import org.junit.Assert.*;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;

/**
 * Simple tests for conversion
 *
 * @author Sergey Vartanov (me@enzet.ru)
 */
public class ConversionTest
{
    @Test
    public void testEscape() throws IOException
    {
        test("\\\\\\{\\}\\[\\]", "\\{}[]");
    }

    @Test
    public void testFormat() throws IOException
    {
        test("\\i {text}", "<i>text</i>");
    }

    public static void test(String input, String output) throws IOException
	{
		Format format = new Format("html");
		
		Scheme scheme = new Scheme(new BufferedReader(new FileReader(new File("default.moirescheme"))));
		format.readFormat(scheme);

        Parser parser = new Parser(input);
		String result = parser.parseInner().convert(format);
		
        Assert.assertEquals(result, output);
    }
}
