pub trait Aliasable: Sized {
    fn unaliased_with_name(&self) -> (Self, Option<String>);

    fn unaliased(&self) -> Self {
        self.unaliased_with_name().0
    }
}

impl Aliasable for String {
    fn unaliased_with_name(&self) -> (Self, Option<String>) {
        (self.clone(), None)
    }
}

impl Aliasable for i64 {
    fn unaliased_with_name(&self) -> (Self, Option<String>) {
        (*self, None)
    }
}

impl Aliasable for f64 {
    fn unaliased_with_name(&self) -> (Self, Option<String>) {
        (*self, None)
    }
}

impl Aliasable for bool {
    fn unaliased_with_name(&self) -> (Self, Option<String>) {
        (*self, None)
    }
}
