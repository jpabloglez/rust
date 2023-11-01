# Rust training application

## Build up
```
docker-compose up -d --build
```

## Compile script
```
docker exec -it rustc src/hello.rs -o build/hello
```

## Run program
```
docker exec -it rust rustc src/hello.rs -o build/hello
```

## Create project
```
cargo new --bin [PROJECT-NAME]
```

## Install dependecies
Add package/s into setup/Cargo.toml file and specify bin directory, then run:
```
docker exec -it rust cargo build
```