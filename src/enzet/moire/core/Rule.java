package enzet.moire.core;

import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;

/**
 * Rule
 *
 * @author Sergey Vartanov (me@enzet.ru)
 */
public class Rule
{
	private String name;
	private int parameters;

	private final Object[] elements;

	class Parameter
	{
		int number;
		boolean isClear;

		public Parameter(int number, boolean isClear)
		{
			this.number = number;
			this.isClear = isClear;
		}
	}

	class Function
	{
		String text;
		boolean isReturn;

		public Function(String text, boolean isReturn)
		{
			for (int i = 0; i < 10; i++)
			{
				text = text.replaceAll("\\\\" + i, "arg" + i);
			}
			this.text = text;
			this.isReturn = isReturn;
		}
	}

	public Rule(String key, String value)
	{
		name = key.substring(0, key.indexOf(" "));
		parameters = Integer.parseInt(key.substring(key.indexOf(" ")).trim());
		elements = parseElements(value);
	}

	public String convert(Word word, Format format)
	{
		StringBuilder returned = new StringBuilder();

		int methods = 0;
		boolean isFirst = false;

		// Invoke first non-returning function

		if (elements.length > 0 && elements[0] instanceof Function)
		{
			if (((Function) elements[0]).isReturn == false)
			{
				methods++;
				invoke(elements[0], new String[parameters * 2], format, methods, returned);
				isFirst = true;
			}
		}
		// Parameters reading

		String[] param = new String[parameters * 2];

		for (int i = 0; i < parameters; i++)
		{
			param[2 * i] = word.getParameter(i, format, false); // converted: 0, 2, 4...
			param[2 * i + 1] = word.getParameter(i, format, true); // clear: 1, 3, 5...
		}

		// Processing other elements

		for (int i = 0; i < elements.length; i++)
		{
			Object element = elements[i];

			if (i == 0 && isFirst) continue;

			if (element instanceof String)
			{
				returned.append(element);
			}
			else if (element instanceof Parameter)
			{
				if (((Parameter) element).isClear)
				{
					returned.append(param[2 * ((Parameter) element).number - 1]);
				}
				else
				{
					returned.append(param[2 * ((Parameter) element).number - 2]);
				}
			}
			else if (element instanceof Function)
			{
				methods++;

				invoke(element, param, format, methods, returned);
			}
		}
		return returned.toString();
	}

	private void invoke(Object element, String[] param, Format format, int methods, StringBuilder returned)
	{
		try
		{
			Class<?> c = Class.forName("enzet.moire.Inner$" + format.name.toUpperCase());
			Class<String> s = String.class;
			Class<?>[] p = new Class[parameters * 2];

			for (int i = 0; i < parameters * 2; i++)
			{
				p[i] = s;
			}
			Method m = c.getMethod("method_" + name + "_" + parameters + "_" + methods, p);

			if (((Function) element).isReturn)
			{
				String result = (String) m.invoke(null, (Object[]) param);
				returned.append(result);
			}
			else
			{
				m.invoke(null, (Object[]) param);
			}
		}
		catch (Exception ex)
		{
			System.err.println("Inner class error.");
			ex.printStackTrace();
		}
	}

	private Object[] parseElements(String text)
	{
		List<Object> elements = new ArrayList<Object>();

		String l = "";

		for (int i = 0; i < text.length(); i++)
		{
			char cp = i > 0 ? text.charAt(i - 1) : ' ';
			char c = text.charAt(i);

			if (cp == '\\')
			{
				l += c;
			}
			else
			{
				switch (c)
				{
					case '\\':
					{
						if (l.length() > 0)
						{
							elements.add(l);
							l = "";
						}
						if (i == text.length() - 1)
						{
							System.err.println("Elements parse error.");
							break;
						}
						char c2 = text.charAt(i + 1);
						if (c2 >= '0' && c2 <= '9')
						{
							elements.add(new Parameter(c2 - '0', false));
							i++;
							break;
						}
						else if (c2 == 'c')
						{
							elements.add(new Parameter(text.charAt(i + 2) - '0', true));
							i += 2;
							break;
						}
						else
						{
							if (c2 == 'n') {l += '\n'; i++;}
							else if (c2 == 't') {l += '\t'; i++;}
							else if (c2 == 'r') {l += '\r'; i++;}
							else if (c2 == 'b') {l += '\b'; i++;}
							else {l += c2; i++;}
						}
						break;
					}
					case '{':
						if (l.length() > 0)
						{
							elements.add(l);
							l = "";
						}
						i++;
						while ((c = text.charAt(i)) != '}')
						{
							l += c;
							i++;
						}
						elements.add(new Function(l, false));
						l = "";
						break;
					case '[':
						if (l.length() > 0)
						{
							elements.add(l);
							l = "";
						}
						i++;
						while ((c = text.charAt(i)) != ']')
						{
							l += c;
							i++;
						}
						elements.add(new Function(l, true));
						l = "";
						break;
					default:
						l += c;
						break;
				}
			}
		}
		if (l.length() > 0)
		{
			elements.add(l);
		}
		return elements.toArray(new Object[elements.size()]);
	}

	public String generateMethods()
	{
		String returned = "";
		int methods = 0;

		for (Object element : elements)
		{
			if (element instanceof Function)
			{
				Function f = (Function) element;

				returned += "\t\tpublic static ";
				returned += f.isReturn ? "String" : "void";
				returned += " method_" + name + "_" + parameters + "_" + ++methods + "(";

				for (int i = 0; i < parameters; i++)
				{
					returned += "String arg" + (i + 1) + ", String carg" + (i + 1);
					if (i != parameters - 1)
					{
						returned += ", ";
					}
				}
				returned += ")\n\t\t{\n\t\t\t";

				if (f.isReturn)
				{
					returned += "return " + f.text + ";";
				}
				else
				{
					returned += f.text;
				}
				returned += "\n\t\t}\n\n";
			}
		}
		return returned;
	}

	// Getters and setters

	public String getName()
	{
		return name;
	}

	public void setName(String name)
	{
		this.name = name;
	}

	public int getParameters()
	{
		return parameters;
	}

	public void setParameters(int parameters)
	{
		this.parameters = parameters;
	}

	@Override
	public String toString()
	{
		return name;
	}
}
