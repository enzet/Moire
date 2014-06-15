package enzet.moire.core;

/**
 * Word type
 *
 * @author Sergey Vartanov (me@enzet.ru)
 */
public enum WordType
{
	/**
	 * Simple word is just text. E.g. <code>white rabbit</code> in
	 * <code>\i {white rabbit}</code>.
	 */
	SIMPLE_WORD,

	/**
	 * Tag is identifier started with <code>\</code>. E.g. <code>\i</code> in
	 * <code>\i {white rabbit}</code>.
	 */
	TAG,

	/**
	 * Branch is one of tag parameters. E.g. <code>{http://enzet.ru}</code> and
	 * <code>author page</code> in
	 * <code>\href {http://enzet.ru} {author page}</code>.
	 */
	BRANCH,

	/**
	 * Formula is text surrounded by <code>$</code>. E.g. <code>$ x^2 $</code>.
	 */
	FORMULA
}
