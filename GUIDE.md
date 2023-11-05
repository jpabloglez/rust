# Rust course
Rust es un lenguaje de programación que se enfoca en la seguridad, la concurrencia y el rendimiento. Fue diseñado para ser práctico, ofreciendo control de bajo nivel sobre la memoria y otras características del sistema, pero sin los riesgos de seguridad que a menudo se asocian con lenguajes como C o C++.

A continuación, te guiaré a través de algunos conceptos básicos de Rust y te proporcionaré ejemplos prácticos.

### Hola Mundo

Comenzaremos con el clásico "Hola Mundo". En Rust, todo programa comienza con una función `main`, que es el punto de entrada del programa.

```rust
fn main() {
    println!("Hola, mundo!");
}
```
### Variables y Mutabilidad

En Rust, las variables son inmutables por defecto. Esto significa que una vez que les asignas un valor, no puedes cambiar ese valor posteriormente. Si quieres hacer una variable mutable, debes usar la palabra clave `mut`.

```rust
fn main() {
    let x = 5;
    println!("El valor de x es: {}", x);
    
    let mut y = 5;
    println!("El valor de y es: {}", y);
    y = 10;
    println!("Ahora el valor de y es: {}", y);
}
```

### Tipos de Datos

Rust es un lenguaje de tipado estático, lo que significa que verifica los tipos de datos en tiempo de compilación. Algunos de los tipos de datos primitivos incluyen `i32` para enteros de 32 bits, `f64` para números de punto flotante de 64 bits, `bool` para valores booleanos y `char` para caracteres.

```rust
fn main() {
    let entero: i32 = 100;
    let flotante: f64 = 10.5;
    let booleano: bool = true;
    let caracter: char = 'a';

    println!("entero: {}, flotante: {}, booleano: {}, caracter: {}", entero, flotante, booleano, caracter);
}
```

### Control de Flujo

Rust utiliza palabras clave comunes para el control de flujo como `if`, `else`, `loop`, `while`, y `for`.

```rust
fn main() {
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

    let a = [10, 20, 30, 40, 50];
    for elemento in a.iter() {
        println!("el valor es: {}", elemento);
    }
}
```

### Funciones

Las funciones en Rust se definen con `fn` y tienen una sintaxis específica para los parámetros y el tipo de valor de retorno.

```rust
fn main() {
    let x = suma(1, 2);
    println!("El resultado de la suma es: {}", x);
}

fn suma(a: i32, b: i32) -> i32 {
    a + b // Rust retorna la última expresión implícitamente, no es necesario usar `return` aquí.
}
```

### Ownership

Uno de los aspectos más únicos de Rust es su sistema de ownership (propiedad). Ownership ayuda a manejar la memoria de manera segura sin necesidad de un recolector de basura. Aquí tienes un ejemplo simple de cómo la propiedad y el préstamo funcionan en Rust:

```rust
fn main() {
    let s1 = String::from("hola");
    let s2 = s1; // s1 ya no es válido después de esta línea, porque s1 "transfiere" su propiedad a s2

    // println!("{}, mundo!", s1); // Esto causaría un error de compilación porque s1 ya no es válido
    println!("{}, mundo!", s2);
}
```

Este código no compilará si intentas usar `s1` después de haberlo movido a `s2`, ya que `s1` ya no posee los datos.

### Concurrency

Rust también tiene excelentes características para escribir software concurrente seguro. Aquí hay un ejemplo muy básico usando hilos:

```rust
use std::thread;
use std::time::Duration;

fn main() {
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
```
Rust tiene muchas características interesantes que son atractivas tanto para programadores de sistemas como para aquellos interesados en aplicaciones web y desarrollo de software en general. Aquí hay algunas características más avanzadas y ejemplos que podrían interesarte:

### Match Control Flow Operator

Rust tiene una poderosa herramienta de control de flujo llamada `match` que permite hacer coincidir un valor con una serie de patrones. Es más poderoso que las construcciones de conmutación (`switch`) que encuentras en otros lenguajes.

```rust
fn main() {
    let valor = 3;

    match valor {
        1 => println!("uno"),
        2 => println!("dos"),
        3 => println!("tres"),
        _ => println!("algo más"),
    }
}
```

### Error Handling

Rust maneja los errores a través de tipos de resultados, usando `Result<T, E>` para devoluciones de funciones que pueden fallar. Esto ayuda a escribir código más robusto y seguro.

```rust
fn main() {
    let resultado = dividir(10.0, 2.0);
    match resultado {
        Ok(valor) => println!("El resultado es: {}", valor),
        Err(e) => println!("Hubo un error: {}", e),
    }
}

fn dividir(numerador: f64, denominador: f64) -> Result<f64, &'static str> {
    if denominador == 0.0 {
        Err("No se puede dividir por cero.")
    } else {
        Ok(numerador / denominador)
    }
}
```

### Enumerations

Rust usa enumeraciones (enums) para trabajar con diferentes tipos de datos que pueden ser uno de varios tipos.

```rust
enum DireccionIp {
    V4(String),
    V6(String),
}

fn main() {
    let cuatro = DireccionIp::V4(String::from("127.0.0.1"));
    let seis = DireccionIp::V6(String::from("::1"));

    // ... uso de cuatro y seis
}
```

### Closures

Las closures son funciones anónimas que puedes almacenar en una variable o pasar como argumentos a otras funciones.

```rust
fn main() {
    let suma = |a: i32, b: i32| -> i32 { a + b };
    println!("La suma es: {}", suma(5, 3));
}
```

### Traits

Los traits en Rust son similares a las interfaces en otros lenguajes: definen un conjunto de métodos que los tipos pueden implementar.

```rust
trait Animal {
    fn nombre(&self) -> String;
}

struct Perro {
    nombre: String,
}

impl Animal for Perro {
    fn nombre(&self) -> String {
        self.nombre.clone()
    }
}

fn main() {
    let perro = Perro { nombre: String::from("Firulais") };
    println!("El animal se llama {}", perro.nombre());
}
```

### Concurrency avanzada

Rust proporciona una forma segura de manejar la concurrencia a través del sistema de ownership y tipos como `Arc` (Atomic Reference Counted) y `Mutex` para manejar el estado compartido.

```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
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

    println!("Resultado: {}", *contador.lock().unwrap());
}
```

### Cargo y Crates

Cargo es el sistema de construcción y gestión de paquetes para Rust. Te permite agregar dependencias (llamadas 'crates') a tu proyecto, que pueden ser bibliotecas de terceros.

```toml
[dependencies]
serde = "1.0"
```

Puedes agregar algo como esto a tu `Cargo.toml` para incluir la crate `serde`, que es una biblioteca de serialización muy conocida en Rust.

Estos son solo algunos ejemplos de las poderosas características de Rust. Si quieres profundizar en alguna de ellas o si tienes un proyecto en mente en el que te gustaría trabajar, ¡házmelo saber!

## Cargo 
Cargo es el gestor de paquetes y sistema de compilación oficial de Rust, y es una herramienta muy poderosa para manejar dependencias y construir proyectos. Aquí te explico cómo usar Cargo para agregar bibliotecas (conocidas como "crates") a tu proyecto de Rust:

### Iniciar un Nuevo Proyecto con Cargo

Primero, para crear un nuevo proyecto de Rust con Cargo, puedes utilizar el siguiente comando en tu terminal:

```sh
cargo new mi_proyecto
```

Esto creará un nuevo directorio llamado `mi_proyecto` con un archivo `Cargo.toml` en su interior, que es donde se definen las dependencias y la configuración del proyecto. También se crea un archivo `src/main.rs` que contiene una función `main` básica.

### Agregar Dependencias

Para agregar una nueva dependencia a tu proyecto, debes editar el archivo `Cargo.toml`. Por ejemplo, si quieres usar la crate `serde` para serializar y deserializar datos, debes agregarla a la sección `[dependencies]` así:

```toml
[dependencies]
serde = "1.0"
```

La versión "1.0" es un indicador de compatibilidad, que le dice a Cargo que deseas una versión que sea compatible con la versión 1.0. Cargo buscará automáticamente la versión más reciente que sea compatible con 1.0 y la instalará.

### Compilar y Construir el Proyecto

Una vez que has agregado tus dependencias, puedes construir tu proyecto usando el comando `cargo build`. Esto compilará tu proyecto junto con todas sus dependencias.

```sh
cargo build
```

Si solo quieres comprobar que tu proyecto se compila sin generar un ejecutable, puedes usar `cargo check`.

```sh
cargo check
```

### Ejecutar el Proyecto

Para ejecutar tu proyecto, puedes usar `cargo run`. Esto compilará tu proyecto (si no está actualizado) y luego ejecutará el binario resultante.

```sh
cargo run
```

### Actualizar las Dependencias

Si deseas actualizar tus crates a la última versión que coincida con los criterios que especificaste en `Cargo.toml`, puedes usar:

```sh
cargo update
```

### Obtener Documentación

Para obtener documentación local de tus dependencias, puedes ejecutar:

```sh
cargo doc --open
```

Esto generará documentación para todas tus dependencias y la abrirá en tu navegador web.

### Publicar un Crate

Si desarrollas una biblioteca y deseas compartirla en [crates.io](https://crates.io/), primero debes registrarte en el sitio, obtener un token de API y luego usar:

```sh
cargo publish
```

Esto empaquetará tu biblioteca y la subirá a crates.io.

### Ejemplo Práctico

Aquí hay un ejemplo de cómo podrías usar una crate en tu archivo `main.rs` después de agregarla a `Cargo.toml`:

```rust
// main.rs
use serde_json::Value;

fn main() {
    let data = r#"
        {
            "name": "John Doe",
            "age": 43,
            "phones": [
                "+44 1234567",
                "+44 2345678"
            ]
        }"#;

    // Parsea la string de datos a `serde_json::Value`.
    let v: Value = serde_json::from_str(data).unwrap();

    // Accede a los campos del objeto JSON.
    println!("Por favor, llama a {} al número {}", v["name"], v["phones"][0]);
}
```

Antes de poder ejecutar este código, debes agregar `serde_json` como dependencia en `Cargo.toml`.

```toml
[dependencies]
serde_json = "1.0"
```

Con estos pasos, deberías poder usar Cargo para manejar dependencias y construir proyectos en Rust con facilidad.