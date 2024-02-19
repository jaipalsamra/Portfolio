function toggleMenu() {
  const menu = document.querySelector(".menu-links");
  const icon = document.querySelector(".hamburger-icon");
  menu.classList.toggle("open");
  icon.classList.toggle("open");
}


// This function will toggle the flip state of the closest flip-container
function toggleFlipState(element) {
  element.closest('.flip-container').querySelector('.flipper').classList.toggle('is-flipped');
}

// Attach event listener to the "Details" button
document.querySelectorAll('.flip-btn').forEach(button => {
  button.addEventListener('click', function() {
    toggleFlipState(this);
  });
});
// Attach event listener to the "Back" button
document.querySelectorAll('.flip-back-btn').forEach(button => {
  button.addEventListener('click', function() {
    toggleFlipState(this);
  });
});

const roles = ["Frontend Dev", "Backend Dev", "Software Dev", "Web Designer"];
let roleIndex = 0;
let letterIndex = 0;
let currentRole = '';
let direction = 'forward';
const roleElement = document.getElementById('role');
roleElement.classList.add('role-cursor'); // Add cursor effect

function typeWriter() {
  if (direction === 'forward') {
    if (letterIndex <= roles[roleIndex].length) {
      currentRole = roles[roleIndex].substring(0, letterIndex++);
      roleElement.textContent = currentRole;
    } else {
      direction = 'backward';
      setTimeout(typeWriter, 2000); // Wait before start erasing
      return;
    }
  } else if (direction === 'backward') {
    if (letterIndex > 0) {
      currentRole = roles[roleIndex].substring(0, --letterIndex);
      roleElement.textContent = currentRole;
    } else {
      direction = 'forward';
      roleIndex = (roleIndex + 1) % roles.length; // Move to the next role
    }
  }
  setTimeout(typeWriter, direction === 'forward' ? 120 : 60); // Faster erase than type
}

typeWriter(); // Start the effect

document.getElementById('checkbox').addEventListener('click', function() {
  if (document.body.getAttribute('data-theme') === 'dark') {
    document.body.setAttribute('data-theme', 'light');
  } else {
    document.body.setAttribute('data-theme', 'dark');
  }
});


document.querySelector('.next-btn').addEventListener('click', function() {
  const currentSet = document.querySelector('.about-containers.current-set');
  const nextSet = document.querySelector('.about-containers.next-set');
  const nextButton = document.querySelector('.next-btn');
  const backButton = document.querySelector('.back-btn');

  // Swipe out the current set
  currentSet.classList.add('swipe-out');

  setTimeout(() => {
    currentSet.style.display = 'none';
    nextSet.style.display = 'flex'; // Make sure this matches your CSS display style for visible sets

    currentSet.classList.remove('current-set', 'swipe-out');
    nextSet.classList.add('current-set', 'swipe-in');
    nextSet.classList.remove('next-set', 'hidden');

    nextButton.style.display = 'none';
    backButton.style.display = 'inline-block';
  }, 500); // Duration matches the swipeOut animation
});

document.querySelector('.back-btn').addEventListener('click', function() {
  const nextSet = document.querySelector('.about-containers.current-set');
  const initialSet = document.querySelector('.about-containers:not(.next-set)');
  const nextButton = document.querySelector('.next-btn');
  const backButton = document.querySelector('.back-btn');

  // Swipe out the next set, but in the reverse direction
  nextSet.classList.add('next-set','swipe-out-reverse'); // You'll define this animation
  setTimeout(() => {
    nextSet.style.display = 'none';
    initialSet.style.display = 'flex'; // Again, ensure this matches your CSS

    nextSet.classList.remove('current-set', 'swipe-out-reverse');
    initialSet.classList.add('current-set', 'swipe-out-reverse');
    initialSet.classList.remove('next-set','hidden');

    // Reverse the button visibility
    nextButton.style.display = 'inline-block';
    backButton.style.display = 'none';
  }, 500); // Ensure this duration matches your new reverse swipe animation
});