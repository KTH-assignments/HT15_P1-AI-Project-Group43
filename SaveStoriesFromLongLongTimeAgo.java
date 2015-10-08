import java.io.*;
import java.net.*;
import javax.swing.text.AttributeSet;
import javax.swing.text.BadLocationException;
import javax.swing.text.Element;
import javax.swing.text.html.*;
import javax.swing.text.html.HTMLDocument.Iterator;
import javax.swing.text.ElementIterator;
import javax.swing.text.StyleConstants;
import java.nio.charset.StandardCharsets;

final class SaveStoriesFromLongLongTimeAgo {
    //LinkedList<String> storyText;
    public static void main(String[] args) {
    	String webpage = args[0];
    	//System.err.println(webpage);
		StringBuilder sb = new StringBuilder();
		String storyTitle = "";
		try {
			InputStream in = new URL(webpage).openConnection().getInputStream(); 
			//System.err.println("Created an InputStream for: "+webpage);  
			InputStreamReader reader = new InputStreamReader(in);
			//System.err.println("Created an InputStreamReader from: "+in);
			try {
				HTMLDocument doc = new HTMLDocument();
				doc.putProperty("IgnoreCharsetDirective", Boolean.TRUE);
				new HTMLEditorKit().read(reader,doc,0);
				//System.err.println("Inserted html stream to: "+doc);
				HTML.Tag t = HTML.Tag.SPAN;
				HTMLDocument.Iterator it = doc.getIterator(t);
				int i = 0;
				if (it != null) {
					while(it.isValid()) {
						if (it.getAttributes().containsAttribute(HTML.Attribute.CLASS, "pageheading")) {
							//System.err.print("Tag: "+it.getTag());
							int startOffset = it.getStartOffset();
							int endOffset = it.getEndOffset();
							int length = endOffset - startOffset;
							String text = doc.getText(startOffset, length);
							sb.append(text+" ");
						}
						it.next();
					}
				} else {
					System.err.println("Could not find any tags: "+t);
				}
			} catch (BadLocationException e) {
				System.err.println(e);
			}
		} catch(IOException e) {
			System.err.println(e);
		}
		try{
			File currDir = new File(".");
			File[] fileList = currDir.listFiles();
			int i = 1;
			String fileName = ".\\auto_corpus";
			String fileType = ".txt";
			for (File f : fileList) {
				//System.err.println("Comparing "+f.toString()+" with "+fileName+fileType);
				while (f.isFile() && f.toString().equals(fileName+fileType)) {
					//System.err.println("File with same name!");
					++i;
					if (i == 2) {
						fileName += i;
					} else {
						fileName = fileName.substring(0, fileName.length() - 1);
						fileName += i;
					}
				}
			}
			fileName += fileType;

			FileOutputStream fos = new FileOutputStream(fileName);
			OutputStreamWriter osw = new OutputStreamWriter(fos, StandardCharsets.UTF_8);

			//PrintWriter out = new PrintWriter(fileName);
			String text = sb.toString().replace("Â", ""); // no idea why this character turns up...
			byte[] bytes = text.getBytes(StandardCharsets.UTF_8);
			byte unwantedA = (byte)0xC382;	// This is the character Â...
			int nToRm = 0;
			int j = 0;
			for (byte b : bytes) {
				if (b==unwantedA) {
					//System.err.println("Found Â!");
					++nToRm;
					//bytes[j] = (byte)0x0020;	// Replace with space character
				}
				++j;
			}
			byte[] newBytes = new byte[bytes.length-nToRm];
			int k = 0;
			for (byte b : bytes) {
				if (b!=unwantedA) {
					newBytes[k] = b;
					++k;
				}
			}
			String properText = new String(newBytes, StandardCharsets.UTF_8);
			/*System.err.println("Did we remove?");
			for (byte b : bytes) {
				if (b==unwantedA) {
					System.err.println("Found Â!");
				}
			}*/
			//out.println(text);
			osw.write(properText);
			osw.close();
			fos.close();
			//out.close();
		} catch(Exception e) {
			System.err.println(e);
		}
    }
}
