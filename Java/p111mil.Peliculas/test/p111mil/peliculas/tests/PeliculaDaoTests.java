package p111mil.peliculas.tests;

import java.util.Calendar;
import java.util.GregorianCalendar;
import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import static org.junit.Assert.*;
import p111mil.peliculas.dao.ConfiguracionHibernate;
import p111mil.peliculas.dao.*;
import p111mil.peliculas.modelo.*;
import p111mil.peliculas.utilidades.ConfiguracionLogger;

/**
 *
 * @author admin
 */
public class PeliculaDaoTests {
    PeliculaDao peliculaDao;
    DirectorDao directorDao;
    PaisDao paisDao;
    ActorDao actorDao;
    
    Pelicula peliculaGuardada;
    Director nuevoDirector;
    Pais nuevoPais;
    Actor nuevoActor1;
    Actor nuevoActor2;
    
    public PeliculaDaoTests() {
        peliculaDao = new PeliculaDao();
        directorDao = new DirectorDao();
        paisDao = new PaisDao();
        actorDao = new ActorDao();
    }
    
    @BeforeClass
    public static void setUpClass() {
        ConfiguracionHibernate.configurar();
        ConfiguracionLogger.configurar();
    }
    
    @AfterClass
    public static void tearDownClass() {
        ConfiguracionHibernate.cerrar();
    }
    
    @Before
    public void setUp() {
        nuevoPais = new Pais();
        nuevoPais.setNombre("Italia");         
        paisDao.guardar(nuevoPais);
        
        nuevoDirector = new Director();
        nuevoDirector.setNombre("Roberto");
        nuevoDirector.setApellido("Benigni");
        nuevoDirector.setGenero("M");
        nuevoDirector.setFechaNacimiento(new GregorianCalendar(1952, Calendar.OCTOBER, 27).getTime());
        nuevoDirector.setPais(nuevoPais);
        directorDao.guardar(nuevoDirector);
        
        nuevoActor1 = new Actor();
        nuevoActor1.setNombre("Roberto");
        nuevoActor1.setApellido("Benigni");
        nuevoActor1.setGenero("M");
        nuevoActor1.setFechaNacimiento(new GregorianCalendar(1952, Calendar.OCTOBER, 27).getTime());
        nuevoActor1.setPais(nuevoPais);
        actorDao.guardar(nuevoActor1);
        
        nuevoActor2 = new Actor();
        nuevoActor2.setNombre("Nicoletta");
        nuevoActor2.setApellido("Braschi");
        nuevoActor2.setGenero("F");
        nuevoActor2.setFechaNacimiento(new GregorianCalendar(1960, Calendar.APRIL, 19).getTime());
        nuevoActor2.setPais(nuevoPais);
        actorDao.guardar(nuevoActor2);
    }
    
    @After
    public void tearDown() {
        if (peliculaGuardada != null) {        
            actorDao.eliminar(nuevoActor1.getId());
            actorDao.eliminar(nuevoActor2.getId());
            peliculaDao.eliminar(peliculaGuardada.getId());
            directorDao.eliminar(nuevoDirector.getId());
            paisDao.eliminar(nuevoPais.getId());
        }
    }

     @Test
     public void Guardar_ConUnaPeliculaNueva_TieneQueInsertarlaEnBaseDeDatos() 
     {
         // Preparar                  
         Pelicula nuevaPelicula = new Pelicula();
         nuevaPelicula.setTitulo("La vita e bella");
         nuevaPelicula.setAnio(1997);
         nuevaPelicula.setPuntuacion(8.6f);
         nuevaPelicula.setDirector(nuevoDirector);
         nuevaPelicula.getActores().add(nuevoActor1);
         nuevaPelicula.getActores().add(nuevoActor2);
         
         // Actuar
         peliculaDao.guardar(nuevaPelicula);
         
         // Afirmar
         peliculaGuardada = peliculaDao.buscarPorId(nuevaPelicula.getId());
         
         assertNotNull(peliculaGuardada);
         assertEquals("La vita e bella", peliculaGuardada.getTitulo());
         assertEquals(1997, peliculaGuardada.getAnio());
         assertEquals(8.6f, peliculaGuardada.getPuntuacion(), 0.0f);
         assertEquals(2, peliculaGuardada.getActores().size());
         assertTrue(peliculaGuardada.getActores().contains(nuevoActor1));
         assertTrue(peliculaGuardada.getActores().contains(nuevoActor2));
     }
     
     @Test
     public void Guardar_ConUnaPeliculaNueva_TieneQueActualizarlaEnBaseDeDatos() 
     {
         // Preparar
        Pelicula nuevaPelicula = new Pelicula();
         nuevaPelicula.setTitulo("La vita e bella");
         nuevaPelicula.setAnio(1997);
         nuevaPelicula.setPuntuacion(8.6f);
         nuevaPelicula.setDirector(nuevoDirector);
         peliculaDao.guardar(nuevaPelicula);
         
         // Actuar
         nuevaPelicula.setTitulo("Pinocho");
         nuevaPelicula.setAnio(2002);
         nuevaPelicula.setPuntuacion(4.3f);
         peliculaDao.guardar(nuevaPelicula);
         
         // Afirmar
         peliculaGuardada = peliculaDao.buscarPorId(nuevaPelicula.getId());
         
         assertEquals("Pinocho", peliculaGuardada.getTitulo());
         assertEquals(2002, peliculaGuardada.getAnio());
         assertEquals(4.3f, peliculaGuardada.getPuntuacion(), 0.0f);
     }
}
