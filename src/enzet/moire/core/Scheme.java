package enzet.moire.core;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Scheme
 * 
 * @author Sergey Vartanov (me@enzet.ru)
 */
public class Scheme
{
    private Section root;
    
    public class Section
    {
        private String name;
        private List<Relation> relations;
        private Section parent;
        private List<Section> children;
        private int level;
        
        class Relation
        {
            public String from;
            public String to;
            
            Relation(String from, String to)
            {
                this.from = from;
                this.to = to;
            }
        }
        
        Section(Section parent, String name, int level)
        {
            children = new ArrayList<Section>();
            relations = new ArrayList<Relation>();
            this.parent = parent;
            this.name = name;
            this.level = level;
        }
        
        void addSection(Section section)
        {
            children.add(section);
        }
        
        void addRelation(String from, String to)
        {
            relations.add(new Relation(from, to));
        }
        
        public void print()
        {
            for (int i = 0; i < level; i++) System.err.print("  ");
            System.out.println(name);
            for (int i = 0; i < level; i++) System.err.print("  ");
            System.err.println(relations);
            for (Section s : children) s.print();
        }
        
        public Section getChild(String name)
        {
            for (Section c : children)
            {
                if (c.name.equals(name)) return c;
            }
            return null;
        }
        
        public String getName()
        {
            return name;
        }
        
        public List<Relation> getRelations()
        {
            return relations;
        }
    }
    
    public Scheme(BufferedReader input) throws IOException
    {
        root = new Section(null, "root", 0);
        
        Section current = root;
        
        String l;
        while ((l = input.readLine()) != null)
        {
            l = l.trim();
            if (l.startsWith(":"))
            {
                int level = 0;
                while (l.length() > level && l.charAt(level) == ':')
                {
                    level++;
                }
                l = l.substring(level).trim();
                
                Section n = new Section(current, l, level);
                if (current.level < level)
                {
                    current.addSection(n);
                }
                else if (current.level == level)
                {
                    current.parent.addSection(n);
                }
                else
                {
                    current.parent.parent.addSection(n);
                }
                current = n;
            }
            else if (!l.equals("") && !l.startsWith("#") && l.contains(":"))
            {
                current.addRelation(l.substring(0, l.indexOf(":")), l.substring(l.indexOf(":") + 1));
            }
        }
    }
    
    public void print()
    {
        root.print();
    }
    
    public Section getRoot()
    {
        return root;
    }
}