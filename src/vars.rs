/*
Variables y Mutabilidad
En Rust, las variables son inmutables por defecto. Esto significa que una vez que les asignas un valor, 
no puedes cambiar ese valor posteriormente. Si quieres hacer una variable mutable, debes usar la palabra 
clave mut. 
*/

fn rvalues() {
    println!("\n=== Variables y Mutabilidad ===");
    let x = 5;
    println!("El valor de x es: {}", x);
    // x = 6; // Esto no compila
    
    let mut y = 5;
    println!("El valor de y es: {}", y);
    y = 10;
    println!("Ahora el valor de y es: {}", y);
    
    // Shadowing
    let z = 5;
    let z = z + 1;
    let z = z * 2;
    println!("El valor de z (shadowing) es: {}", z);
}

/* Tipos de Datos
 Rust es un lenguaje de tipado estático, lo que significa que verifica los tipos de 
datos en tiempo de compilación. Algunos de los tipos de datos primitivos incluyen i32 
para enteros de 32 bits, f64 para números de punto flotante de 64 bits, bool para 
valores booleanos y char para caracteres.
*/

fn rtypes() {
    println!("\n=== Tipos de datos ===");
    // Tipos escalares
    let entero: i32 = 100;
    let flotante: f64 = 10.5;
    let booleano: bool = true;
    let caracter: char = 'a';
    
    println!("entero: {}, flotante: {}, booleano: {}, caracter: {}", entero, flotante, booleano, caracter);
    
    // Tipos compuestos
    // Tuplas
    let tupla: (i32, f64, u8) = (500, 6.4, 1);
    let (x, y, z) = tupla; // Desestructuración
    println!("Los valores de la tupla son: {}, {}, {}", x, y, z);
    
    // Arreglos
    let arreglo = [1, 2, 3, 4, 5];
    let meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo"];
    println!("El primer mes es: {}", meses[0]);
    println!("El tercer elemento del arreglo es: {}", arreglo[2]);
}

/* Control de Flujo
Rust utiliza palabras clave comunes para el control de flujo como if, else, loop, while, y for.
*/
fn rflux() {
    println!("\n=== Control de flujo ===");
    let num = 7;

    if num < 5 {
        println!("la condición fue verdadera");
    } else if num == 5 {
        println!("el número es 5");
    } else {
        println!("la condición fue falsa");
    }
    
    // Expresión if
    let condicion = true;
    let numero = if condicion { 5 } else { 6 };
    println!("El valor del número es: {}", numero);

    // loop
    let mut contador = 0;
    let resultado = loop {
        contador += 1;
        
        if contador == 10 {
            break contador * 2;
        }
    };
    println!("El resultado es: {}", resultado);

    // while
    let mut numero = 3;
    while numero != 0 {
        println!("{}!", numero);
        numero -= 1;
    }
    println!("LIFTOFF!!!");

    println!("\n - Iteración:");
    let a = [10, 20, 30, 40, 50];
    for elemento in a.iter() {
        println!("el valor es: {}", elemento);
    }

    println!("\n - Rango:");
    for a in (1..4).rev() {
        println!("{}!", a);
    }
    println!("LIFTOFF!!!");
}

/* Funciones
Las funciones en Rust se definen con fn y tienen una sintaxis específica para 
los parámetros y el tipo de valor de retorno.
*/
fn rsuma(s1: i32, s2: i32) -> i32 {
    println!("\n=== Funciones ===");
    let suma = s1 + s2; // Rust retorna la última expresión implícitamente, no es necesario usar `return` aquí.
    println!("El resultado de la suma es: {}", suma);
    suma // Retorno implícito
}

fn suma_con_tipos() {
    let edad: u8 = 25;
    let altura: f32 = 1.75;
    
    let resultado = edad + altura;
    println!("Resultado: {}", resultado);
}

// Función con múltiples parámetros
fn imprime_labeled_measurement(value: i32, unit_label: char) {
    println!("La medida es: {}{}", value, unit_label);
}

/* Match Control Flow Operator
Rust tiene una poderosa herramienta de control de flujo llamada `match` que permite 
hacer coincidir un valor con una serie de patrones. 
*/
fn rmatch() {
    println!("\n=== Match Control Flow ===");
    let valor = 3;

    match valor {
        1 => println!("uno"),
        2 => println!("dos"),
        3 => println!("tres"),
        _ => println!("algo más"), // _ es el catch-all pattern
    }
    
    // Match con Option<T>
    let cinco = Some(5);
    let seis = plus_one(cinco);
    let _ninguno = plus_one(None);  // Prefixed with _ to suppress warning
    
    match seis {
        Some(n) => println!("Seis es: {}", n),
        None => println!("No hay valor"),
    }
}

fn plus_one(x: Option<i32>) -> Option<i32> {
    match x {
        None => None,
        Some(i) => Some(i + 1),
    }
}

/* Enumerations
Rust usa enumeraciones (enums) para trabajar con diferentes tipos de datos que pueden ser uno de varios tipos.
*/
fn renums() {
    println!("\n=== Enumerations ===");
    
    enum IpAddrKind {
        V4,
        V6,
    }
    
    struct IpAddr {
        kind: IpAddrKind,
        address: String,
    }
    
    let home = IpAddr {
        kind: IpAddrKind::V4,
        address: String::from("127.0.0.1"),
    };
    
    let loopback = IpAddr {
        kind: IpAddrKind::V6,
        address: String::from("::1"),
    };
    
    println!("Home IP: {:?}", home.address);
    println!("Loopback IP: {:?}", loopback.address);
    
    // Enum con valores asociados
    enum Message {
        Quit,
        Move { x: i32, y: i32 },
        Write(String),
        ChangeColor(i32, i32, i32),
    }
    
    let msg1 = Message::Write(String::from("hello"));
    let _msg2 = Message::Move { x: 10, y: 20 };  // Prefixed with _ to suppress warning
    
    // Implementación de métodos en enums
    impl Message {
        fn call(&self) {
            // Método para llamar al mensaje
            println!("Mensaje procesado");
        }
    }
    
    msg1.call();
}

/*Uno de los aspectos más únicos de Rust es su sistema de ownership (propiedad). Ownership ayuda 
a manejar la memoria de manera segura sin necesidad de un recolector de basura. 
Aquí tienes un ejemplo simple de cómo la propiedad y el préstamo funcionan en Rust:*/

fn rowner() {
    println!("\n=== Ownership ===");
    let s1 = String::from("hola");
    let s2 = s1; // s1 ya no es válido después de esta línea, porque s1 "transfiere" su propiedad a s2

    // println!("{}, mundo!", s1); // Esto causaría un error de compilación porque s1 ya no es válido
    println!("{}, mundo!", s2);
    
    // Borrowing (préstamo)
    let s3 = String::from("hello");
    let len = calculate_length(&s3); // Pasamos una referencia, no la propiedad
    println!("La longitud de '{}' es {}.", s3, len);
    
    // Mutable borrowing
    let mut s4 = String::from("hola");
    change(&mut s4);
    println!("La cadena modificada es: {}", s4);
}

fn calculate_length(s: &String) -> usize {
    s.len()
}

fn change(s: &mut String) {
    s.push_str(", mundo");
}

/* Error Handling
Rust maneja los errores a través de tipos de resultados, usando `Result<T, E>` para devoluciones 
de funciones que pueden fallar. 
*/
fn rerror() {
    println!("\n=== Error Handling ===");
    
    let resultado = dividir(10.0, 2.0);
    match resultado {
        Ok(valor) => println!("El resultado es: {}", valor),
        Err(e) => println!("Hubo un error: {}", e),
    }
    
    // Usando unwrap (solo para ejemplos, no recomendado en producción)
    let resultado2 = dividir(10.0, 0.0).unwrap_or(0.0);
    println!("Resultado con unwrap_or: {}", resultado2);
}

fn dividir(numerador: f64, denominador: f64) -> Result<f64, &'static str> {
    if denominador == 0.0 {
        Err("No se puede dividir por cero.")
    } else {
        Ok(numerador / denominador)
    }
}

/* Closures
Las closures son funciones anónimas que puedes almacenar en una variable o pasar como argumentos 
a otras funciones.
*/
fn rclosures() {
    println!("\n=== Closures ===");
    
    let suma = |a: i32, b: i32| -> i32 { a + b };
    println!("La suma con closure es: {}", suma(5, 3));
    
    let x = 4;
    let igual_que_x = |z| z == x; // Captura x del entorno
    let y = 4;
    println!("¿{} es igual que {}? {}", y, x, igual_que_x(y));
}

/* Concurrency
Rust también tiene excelentes características para escribir software concurrente seguro. 
Aquí hay un ejemplo muy básico usando hilos:*/

use std::thread;
use std::time::Duration;
use std::sync::{Arc, Mutex};

fn rthread() {
    println!("\n=== Concurrency ===");
    
    // Ejemplo básico de hilos
    let handle = thread::spawn(|| {
        for i in 1..10 {
            println!("número {} desde el hilo secundario!", i);
            thread::sleep(Duration::from_millis(1));
        }
    });

    for i in 1..5 {
        println!("número {} desde el hilo principal!", i);
        thread::sleep(Duration::from_millis(1));
    }
    
    handle.join().unwrap(); // Esperar a que el hilo secundario termine
    
    // Ejemplo con Arc y Mutex para compartir estado
    let contador = Arc::new(Mutex::new(0));
    let mut hilos = vec![];

    for _ in 0..10 {
        let contador = Arc::clone(&contador);
        let hilo = thread::spawn(move || {
            let mut num = contador.lock().unwrap();
            *num += 1;
        });
        hilos.push(hilo);
    }

    for hilo in hilos {
        hilo.join().unwrap();
    }

    println!("Resultado del contador compartido: {}", *contador.lock().unwrap());
}

fn main(){
    println!("=== Rust Training Application ===");
    rvalues();
    rtypes();
    rflux();
    rsuma(1, 4);
    suma_con_tipos();
    imprime_labeled_measurement(5, 'h');
    rmatch();
    renums();
    rowner();
    rerror();
    rclosures();
    rthread();
    println!("\n=== Fin del entrenamiento ===");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_rsuma() {
        assert_eq!(rsuma(2, 3), 5);
        assert_eq!(rsuma(-1, 1), 0);
        assert_eq!(rsuma(0, 0), 0);
    }

    #[test]
    fn test_plus_one() {
        assert_eq!(plus_one(Some(5)), Some(6));
        assert_eq!(plus_one(None), None);
    }

    #[test]
    fn test_dividir() {
        assert_eq!(dividir(10.0, 2.0), Ok(5.0));
        assert!(dividir(10.0, 0.0).is_err());
    }
}