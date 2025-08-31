#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_suma() {
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