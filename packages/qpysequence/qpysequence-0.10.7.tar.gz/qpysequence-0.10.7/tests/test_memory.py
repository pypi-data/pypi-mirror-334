import pytest

from qpysequence.program import Register
from qpysequence.program.memory import Memory


@pytest.fixture(name="memory")
def fixture_memory() -> Memory:
    """Loads Program

    Returns:
        Program: Instance of the Program class
    """
    return Memory(max_registers=2)


class TestRegister:
    """Unitary tests checking the Register class behavior"""

    def test_init(self):
        """Test init works correctly."""
        register = Register()

        assert register.number == Register.NOT_ALLOCATED
        assert not register.allocated

    def test_allocate_deallocate(self):
        """Tests that allocation and deallocation work correctly."""
        register = Register()
        register.allocate(123)

        assert register.number == 123
        assert register.allocated

        register.deallocate()

        assert register.number == Register.NOT_ALLOCATED
        assert not register.allocated


class TestMemory:
    """Unitary tests checking the Memory class behavior"""

    def test_allocate_register_and_mark_in_use(self, memory: Memory):
        """Tests that a Memory allocates registers properly."""

        register_a = Register()
        register_b = Register()

        memory.allocate_register_and_mark_in_use(register_a)
        memory.allocate_register_and_mark_in_use(register_b)

        assert register_a.allocated
        assert register_b.allocated
        assert register_a.number == 0
        assert register_b.number == 1

        assert memory.registry[0]
        assert memory.registry[1]

    def test_allocating_same_register_twice_does_not_do_anything(self, memory: Memory):
        """Tests that allocating a register two or more times doesn't do anything."""
        register_a = Register()
        memory.allocate_register_and_mark_in_use(register_a)

        assert register_a.allocated
        assert register_a.number == 0
        assert memory.registry[0]

        memory.allocate_register_and_mark_in_use(register_a)
        assert register_a.allocated
        assert register_a.number == 0
        assert memory.registry[0]

    def test_allocate_register_throws_error_if_registry_is_full(self, memory: Memory):
        """Tests that a Memory throws error if registery is full when allocating a register."""
        register_a = Register()
        register_b = Register()
        register_c = Register()

        memory.allocate_register_and_mark_in_use(register_a)
        memory.allocate_register_and_mark_in_use(register_b)

        with pytest.raises(MemoryError):
            memory.allocate_register_and_mark_in_use(register_c)

    def test_mark_in_use_mark_out_of_use(self, memory: Memory):
        """Tests that a Memory marks registers as in-use and out-of-use properly."""

        register_a = Register()

        memory.allocate_register_and_mark_in_use(register_a)

        assert register_a.allocated
        assert memory.registry[0]

        memory.mark_out_of_use(register_a)

        assert register_a.allocated
        assert not memory.registry[0]

        memory.mark_in_use(register_a)

        assert register_a.allocated
        assert memory.registry[0]
