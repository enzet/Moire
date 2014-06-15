	// Build-in methods

	/**
	 * Warning message
	 */
	public static void warning(String message)
	{
		System.out.println("Warning: " + message + ".");
	}

	/**
	 * Repeat string
	 */
	public static String multiline(int number, String loop)
	{
		StringBuilder builder = new StringBuilder();

		for (int i = 0; i < number; i++)
		{
			builder.append(loop);
		}
		return builder.toString();
	}
