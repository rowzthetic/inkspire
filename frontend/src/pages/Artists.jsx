import '../App.css';

export default function Artists() {
  return (
    <section className="artists">
        <h2>Meet Our Artists</h2>
        <div className="artist-cards">
            <div className="card">
                <img src="images/artist.JPG" alt="Artist 1" />
                <h3>Rajendra Khadgi</h3>
                <p>Specializes in realism & portrait tattoos.</p>
            </div>
            <div className="card">
                <img src="images/artist2.jpg" alt="Artist 2" />
                <h3>Rajesh Hamal</h3>
                <p>Expert in fine line & minimalist designs.</p>
            </div>
            <div class="card">
                <img src="images/artist3.jpg" alt="Artist 3" />
                <h3>Bhuwan K.c</h3>
                <p>Bold traditional & neo-traditional styles.</p>
            </div>
        </div>
    </section>
  );
}