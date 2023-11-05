/*
Variables y Mutabilidad
En Rust, las variables son inmutables por defecto. Esto significa que una vez que les asignas un valor, 
no puedes cambiar ese valor posteriormente. Si quieres hacer una variable mutable, debes usar la palabra 
clave mut. 
*/

fn rvalues() {
    println!("\n - Variables y Mutabilidad");
    let x = 5;
    println!("El valor de x es: {}", x);
    // x = 6; // Esto no compila
    
    let mut y = 5;
    println!("El valor de y es: {}", y);
    y = 10;
    println!("Ahora el valor de y es: {}", y);
}

/* Tipos de Datos
 Rust es un lenguaje de tipado estático, lo que significa que verifica los tipos de 
datos en tiempo de compilación. Algunos de los tipos de datos primitivos incluyen i32 
para enteros de 32 bits, f64 para números de punto flotante de 64 bits, bool para 
valores booleanos y char para caracteres.
*/

fn rtypes() {
    println!("\n - Tipos de datos");
    let entero: i32 = 100;
    let flotante: f64 = 10.5;
    let booleano: bool = true;
    let caracter: char = 'a';

    println!("entero: {}, flotante: {}, booleano: {}, caracter: {}", entero, flotante, booleano, caracter);
}

/* Control de Flujo
Rust utiliza palabras clave comunes para el control de flujo como if, else, loop, while, y for.
*/
fn rflux() {
    println!("\n - Control de flujo");
    let num = 7;

    if num < 5 {
        println!("la condición fue verdadera");
    } else {
        println!("la condición fue falsa");
    }

    loop {
        println!("esto se imprimirá para siempre");
        break; // Comentando esta línea, el loop será infinito
    }

    println!("\n - Iteración:");
    let a = [10, 20, 30, 40, 50];
    for elemento in a.iter() {
        println!("el valor es: {}", elemento);
    }

    println!("\n - Rango:");
    for a in 0..5 {
        println!("el valor es: {}", a);
    }
}

/* Funciones
Las funciones en Rust se definen con fn y tienen una sintaxis específica para 
los parámetros y el tipo de valor de retorno.
*/
fn rsuma(s1: i32, s2: i32) -> i32 {
    println!("\n - Funciones");
    let suma = s1 + s2; // Rust retorna la última expresión implícitamente, no es necesario usar `return` aquí.
    println!("El resultado de la suma es: {}", suma);
    return suma;
}

/*Uno de los aspectos más únicos de Rust es su sistema de ownership (propiedad). Ownership ayuda 
a manejar la memoria de manera segura sin necesidad de un recolector de basura. 
Aquí tienes un ejemplo simple de cómo la propiedad y el préstamo funcionan en Rust:*/

fn rowner() {
    println!("\n - Ownership");
    let s1 = String::from("hola");
    let s2 = s1; // s1 ya no es válido después de esta línea, porque s1 "transfiere" su propiedad a s2

    // println!("{}, mundo!", s1); // Esto causaría un error de compilación porque s1 ya no es válido
    println!("{}, mundo!", s2);
}

/* Concurrency
Rust también tiene excelentes características para escribir software concurrente seguro. 
Aquí hay un ejemplo muy básico usando hilos:*/

use std::thread;
use std::time::Duration;

fn rthread() {
    println!("\n - Concurrency");
    thread::spawn(|| {
        for i in 1..10 {
            println!("número {} desde el hilo secundario!", i);
            thread::sleep(Duration::from_millis(1));
        }
    });

    for i in 1..5 {
        println!("número {} desde el hilo principal!", i);
        thread::sleep(Duration::from_millis(1));
    }
}

fn main(){
    rvalues();
    rtypes();
    rflux();
    rsuma(1, 4);
    rowner();
    rthread();
}