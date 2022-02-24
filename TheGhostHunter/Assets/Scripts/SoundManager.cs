using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SoundManager : MonoBehaviour
{
    public AudioClip BGM;
    public AudioClip UseItemSoundEffect;
    public AudioClip BuyItemSoundEffect;
    public AudioClip SelltemSoundEffect;
    public AudioClip ClickSoundEffect;
    public AudioClip CatSoundEffect;
    public AudioClip AttackSoundEffect;
    public AudioClip HitSoundEffect;
    public AudioClip NextPageSoundEffect;

    AudioSource soundEffectPlayer;
    float volume = 0.7f;
    float time = 0;

    static public SoundManager instance;
    private void Awake()
    {
        instance = this;
    }

    private void Start()
    {
        soundEffectPlayer = GetComponent<AudioSource>();
    }

    public void PlaySound(AudioClip clip)
    {
        soundEffectPlayer.Stop();

        soundEffectPlayer.clip = clip;
        soundEffectPlayer.volume = volume;
        soundEffectPlayer.loop = false;

        soundEffectPlayer.time = time;
        soundEffectPlayer.Play();
    }

    public AudioClip SelectSound(string soundName)
    {
        AudioClip sound = UseItemSoundEffect;

        switch (soundName)
        {
            case "UseItem":
                sound = UseItemSoundEffect;
                volume = 1;
                time = 1f;
                break;
            case "BuyItem":
                sound = BuyItemSoundEffect;
                volume = 1;
                time = 0f;
                break;
            case "SellItem":
                sound = SelltemSoundEffect;
                volume = 1;
                time = 0f;
                break;
            case "Click":
                sound = ClickSoundEffect;
                volume = 1;
                time = 1f;
                break;
            case "Cat":
                sound = CatSoundEffect;
                volume = 1;
                time = 0f;
                break;
            case "Attack":
                sound = AttackSoundEffect;
                time = 0f;
                volume = 0.7f;
                break;
            case "Hit":
                sound = HitSoundEffect;
                time = 1f;
                volume = 0.7f;
                break;
            case "NextPage":
                sound = NextPageSoundEffect;
                time = 0f;
                volume = 0.7f;
                break;
        }

        return sound;
    }

}//End Class
