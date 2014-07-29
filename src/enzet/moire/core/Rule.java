package enzet.moire.core;

import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;

/**
 * Rule. Tag to format translation.
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

		@Override
		public String toString()
		{
			return "argument " + number + ", " + (isClear ? "" : "not") +
					" clear";
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

		@Override
		public String toString()
		{
			return (isReturn ? "" : "not ") + "returned: " + text;
		}
	}

	public Rule(String key, String value)
	{
		name = key.substring(0, key.indexOf(" "));
		parameters = Integer.parseInt(key.substring(key.indexOf(" ")).trim());
		elements = parseElements(value);
	}

	public String convert(Word word, Format format, State state)
	{
		StringBuilder returned = new StringBuilder();

		int methods = 0;
		boolean isFirst = false;

		// Invoke first non-returning function

		if (elements.length > 0 && elements[0] instanceof Function)
		{
			if (!((Function) elements[0]).isReturn)
			{
				methods++;
				invoke(elements[0], new Object[parameters * 2 + 1], format,
						methods, returned);
				isFirst = true;
			}
		}
		// Parameters reading

		int size = parameters * 2 + 1;

		Object[] param = new Object[size];

		List<Word> childrenParameter;

		if (word.children != null && word.children.size() > 0 &&
				word.children.get(0) != null)
		{
			try
			{
				childrenParameter = word.children.get(0).children;
			}
			catch (Exception e)
			{
				childrenParameter = new ArrayList<Word>();
			}
		}
		else
		{
			childrenParameter = new ArrayList<Word>();
		}
		state.setChildren(childrenParameter);
		param[0] = state;

		for (int i = 0; i < parameters; i++)
		{
			/* converted: 1, 3, 5... */
			param[2 * i + 1] = word.getParameter(i, format, false, state);

			/* clear: 2, 4, 6... */
			param[2 * i + 2] = word.getParameter(i, format, true, state);
		}
		/*
		 * Elements processing
		 */
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
					if (2 * ((Parameter) element).number < size)
					{
						returned.append(
								param[2 * ((Parameter) element).number]);
					}
					else
					{
						System.err.println("Error: too many arguments for " +
								"rule " + name + ": " +
								((Parameter) element).number);
					}
				}
				else
				{
					if (2 * ((Parameter) element).number - 1 < size)
					{
						returned.append(
								param[2 * ((Parameter) element).number - 1]);
					}
					else
					{
						System.err.println("Error: too many arguments for " +
								"rule " + name + ": " +
								((Parameter) element).number);
					}
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

	private void invoke(Object element, Object[] param, Format format,
			int methods, StringBuilder returned)
	{
		try
		{
			Class<?>[] p = new Class[parameters * 2 + 1];

			p[0] = State.class;

			for (int i = 1; i < parameters * 2 + 1; i++)
			{
				p[i] = String.class;
			}
			Method m = getMethod(format, methods, p);

			if (m == null)
			{
				return;
			}
			if (((Function) element).isReturn)
			{
				String result = (String) m.invoke(null, param);
				returned.append(result);
			}
			else
			{
				m.invoke(null, param);
			}
		}
		catch (Exception ex)
		{
			System.err.println("Inner class error.");
			ex.printStackTrace();
		}
	}

	private Method getMethod(Format format, int methodNumber, Class<?>[] p)
	{
		Method m;
		Class<?> c;

		try
		{
			c = Class.forName("enzet.moire.Inner$" +
					format.getName().toUpperCase());
		}
		catch (ClassNotFoundException e)
		{
			System.err.println("Class enzet.moire.Inner$" +
					format.getName().toUpperCase() + " not found.");
			return null;
		}
		try
		{
			m = c.getMethod("method_" + name + "_" + parameters + "_" +
					methodNumber, p);
		}
		catch (NoSuchMethodException e)
		{
			if (format.parent != null)
			{
				return getMethod(format.parent, methodNumber, p);
			}
			System.err.println("Class enzet.moire.Inner$" +
					format.getName().toUpperCase() + " has no method for " +
					name + ".");

			return null;
		}
		return m;
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
							elements.add(new Parameter(text.charAt(i + 2) -
									'0', true));
							i += 2;
							break;
						}
						else
						{
							if (c2 == 'n') {l += '\n';}
							else if (c2 == 't') {l += '\t';}
							else if (c2 == 'r') {l += '\r';}
							else if (c2 == 'b') {l += '\b';}
							else {l += c2;}
							i++;
						}
						break;
					}
					case '{':
						if (i == 0 || text.charAt(i - 1) != '\\')
						{
							if (l.length() > 0)
							{
								elements.add(l);
								l = "";
							}
							i++;
							int k = 0;
							while (!((c = text.charAt(i)) == '}' && k == 0 && 
									text.charAt(i - 1) != '\\'))
							{
								if (c == '{') k++;
								if (c == '}') k--;
								l += c;
								i++;
							}
							elements.add(new Function(l, false));
							l = "";
							break;
						}
					case '[':
						if (i == 0 || text.charAt(i - 1) != '\\')
						{
							if (l.length() > 0)
							{
								elements.add(l);
								l = "";
							}
							i++;
							int kk = 0;
							while (!((c = text.charAt(i)) == ']' && kk == 0 &&
									text.charAt(i - 1) != '\\'))
							{
								if (c == '[') kk++;
								if (c == ']') kk--;
								l += c;
								i++;
							}
							elements.add(new Function(l, true));
							l = "";
							break;
						}
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
		StringBuilder returned = new StringBuilder();
		int methods = 0;

		for (Object element : elements)
		{
			if (element instanceof Function)
			{
				Function f = (Function) element;

				returned.append("\t\tpublic static ")
						.append(f.isReturn ? "String" : "void")
						.append(" method_").append(name).append("_")
						.append(parameters).append("_").append(++methods)
						.append("(").append("State state")
						.append(parameters == 0 ? "" : ", ");

				for (int i = 0; i < parameters; i++)
				{
					returned.append("String arg").append(i + 1)
							.append(", String carg").append(i + 1);

					if (i != parameters - 1)
					{
						returned.append(", ");
					}
				}
				returned.append(")\n\t\t{\n\t\t\t").append(f.text)
						.append("\n\t\t}\n\n");
			}
		}
		return returned.toString();
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
		StringBuilder returned = new StringBuilder(name).append("\n");

		for (Object element : elements)
		{
			returned.append("    ").append(element).append("\n");
		}
		return returned.toString();
	}
}
